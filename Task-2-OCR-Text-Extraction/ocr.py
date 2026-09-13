import os
import shutil
import pytesseract
from PIL import Image
import numpy as np
from utils import clean_ocr_text

# Configure Tesseract CMD from environment variable if set
TESSERACT_CMD_ENV = os.environ.get('TESSERACT_CMD')
if TESSERACT_CMD_ENV and os.path.exists(TESSERACT_CMD_ENV):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_ENV
else:
    # Common installation paths check
    possible_paths = [
        "/usr/local/bin/tesseract",
        "/usr/bin/tesseract",
        "/opt/homebrew/bin/tesseract",
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break


def is_tesseract_available():
    """
    Check if the Tesseract OCR binary is installed and executable via pytesseract.
    Returns (available: bool, status_message: str).
    """
    try:
        version = pytesseract.get_tesseract_version()
        return True, f"Tesseract v{version} is installed and available."
    except Exception as e:
        # Also check shutil.which
        tesseract_in_path = shutil.which('tesseract')
        if tesseract_in_path:
            try:
                pytesseract.pytesseract.tesseract_cmd = tesseract_in_path
                version = pytesseract.get_tesseract_version()
                return True, f"Tesseract v{version} detected at {tesseract_in_path}."
            except Exception:
                pass

        return False, (
            "Tesseract OCR is not installed or could not be found in system PATH. "
            "Please install Tesseract OCR and ensure it is accessible to pytesseract."
        )


def calculate_ocr_confidence(image_input):
    """
    Calculate average word confidence score using pytesseract.image_to_data.
    Returns float score (0-100) or None if calculation fails.
    """
    try:
        if isinstance(image_input, str):
            img = Image.open(image_input)
        elif isinstance(image_input, np.ndarray):
            img = Image.fromarray(image_input)
        else:
            img = image_input

        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        confidences = []
        if 'conf' in data:
            for conf, text in zip(data['conf'], data['text']):
                # Filter out -1 conf values and empty/whitespace text blocks
                if conf != -1 and text and text.strip():
                    confidences.append(float(conf))

        if confidences:
            avg_conf = sum(confidences) / len(confidences)
            return round(avg_conf, 1)
        return None
    except Exception:
        return None


def extract_text_tesseract(image_input, lang='eng', config='--psm 3'):
    """
    Extract text from image using Tesseract OCR.
    
    Parameters:
        image_input: File path, numpy array, or PIL Image object.
        lang: Language model code (default 'eng').
        config: Page segmentation mode config.

    Returns:
        dict containing 'text', 'confidence', 'status', and 'engine'.
    """
    available, msg = is_tesseract_available()
    if not available:
        return {
            "success": False,
            "engine": "Tesseract OCR",
            "text": "",
            "confidence": None,
            "error": msg
        }

    try:
        if isinstance(image_input, str):
            img = Image.open(image_input)
        elif isinstance(image_input, np.ndarray):
            img = Image.fromarray(image_input)
        else:
            img = image_input

        raw_text = pytesseract.image_to_string(img, lang=lang, config=config)
        cleaned_text = clean_ocr_text(raw_text)
        confidence = calculate_ocr_confidence(img)

        if not cleaned_text:
            return {
                "success": True,
                "engine": "Tesseract OCR",
                "text": "No readable text was detected in the image.",
                "confidence": confidence,
                "warning": "Empty OCR output"
            }

        return {
            "success": True,
            "engine": "Tesseract OCR",
            "text": cleaned_text,
            "confidence": confidence,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "engine": "Tesseract OCR",
            "text": "",
            "confidence": None,
            "error": f"Tesseract execution error: {str(e)}"
        }
