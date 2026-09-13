import os
import re
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit


def allowed_file(filename):
    """Check if file extension is allowed."""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def validate_image_file(file_path):
    """
    Validate that an uploaded file exists, is non-empty, fits size constraints,
    has a valid extension, and can be opened as a valid image by PIL.
    Returns (is_valid, error_message).
    """
    if not os.path.exists(file_path):
        return False, "Uploaded file does not exist on server."

    size = os.path.getsize(file_path)
    if size == 0:
        return False, "Uploaded file is empty."
    if size > MAX_FILE_SIZE_BYTES:
        return False, f"File size exceeds limit of {MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB."

    ext = file_path.rsplit('.', 1)[-1].lower() if '.' in file_path else ''
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file format (.{ext}). Please upload JPG, JPEG, PNG, BMP, or TIFF."

    try:
        with Image.open(file_path) as img:
            img.verify()
        # Re-open after verify to ensure headers are readable
        with Image.open(file_path) as img:
            img.load()
    except Exception as e:
        return False, f"Invalid or corrupted image file: {str(e)}"

    return True, None


def clean_ocr_text(raw_text):
    """
    Clean extracted OCR text cleanly without losing structure:
    - Normalizes excessive blank lines (max 2 consecutive newlines).
    - Trims trailing whitespace on each line.
    - Removes non-printable control characters except standard whitespace.
    - Preserves meaningful line breaks, punctuation, and numbers.
    """
    if not raw_text:
        return ""

    # Replace non-printable ASCII control chars except newline, tab, carriage return
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', raw_text)

    # Split lines and rstrip each line
    lines = [line.rstrip() for line in cleaned.splitlines()]

    # Rejoin with standard newlines
    joined = "\n".join(lines)

    # Collapse 3+ consecutive newlines to 2
    joined = re.sub(r'\n{3,}', '\n\n', joined)

    return joined.strip()


def sanitize_filename(filename):
    """Generate a safe, unique filename for uploaded images."""
    base_name = secure_filename(filename)
    if not base_name:
        base_name = "uploaded_image.png"
    return base_name
