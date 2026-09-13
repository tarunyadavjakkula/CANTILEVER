import os
import shutil
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from utils import validate_image_file, clean_ocr_text, sanitize_filename, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES
from preprocessing import preprocess_image
from ocr import extract_text_tesseract, is_tesseract_available
from gemma_ocr import extract_text_gemma, check_gemma_availability

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DATASET_FOLDER = os.path.join(BASE_DIR, "dataset")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASET_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_BYTES


def get_available_samples():
    """List sample dataset files available for testing."""
    if not os.path.exists(DATASET_FOLDER):
        return []
    files = [f for f in os.listdir(DATASET_FOLDER) if f.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS]
    return sorted(files)


@app.route('/', methods=['GET'])
def index():
    tess_ok, tess_msg = is_tesseract_available()
    gemma_ok, gemma_model, gemma_msg = check_gemma_availability()
    sample_files = get_available_samples()

    return render_template(
        'index.html',
        tesseract_available=tess_ok,
        tesseract_message=tess_msg,
        gemma_available=gemma_ok,
        gemma_model=gemma_model,
        gemma_message=gemma_msg,
        samples=sample_files
    )


@app.route('/api/status', methods=['GET'])
def status():
    tess_ok, tess_msg = is_tesseract_available()
    gemma_ok, gemma_model, gemma_msg = check_gemma_availability()
    return jsonify({
        "tesseract": {"available": tess_ok, "message": tess_msg},
        "gemma": {"available": gemma_ok, "model": gemma_model, "message": gemma_msg}
    })


@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/dataset/<path:filename>')
def serve_dataset(filename):
    return send_from_directory(DATASET_FOLDER, filename)


@app.route('/extract', methods=['POST'])
def extract():
    """
    Process image upload or dataset sample selection, run optional OpenCV
    preprocessing, and perform OCR text extraction.
    """
    engine = request.form.get('engine', 'tesseract').lower()
    use_preprocessing = request.form.get('use_preprocessing', 'true').lower() in ('true', '1', 'on', 'yes')
    sample_choice = request.form.get('sample_choice', '').strip()

    saved_image_path = None
    display_image_url = None
    original_filename = ""

    # Check if a file was uploaded
    if 'image_file' in request.files and request.files['image_file'].filename:
        file = request.files['image_file']
        original_filename = file.filename
        safe_name = sanitize_filename(original_filename)
        saved_image_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
        file.save(saved_image_path)
        display_image_url = f"/uploads/{safe_name}"

    # Or if a sample dataset file was selected
    elif sample_choice:
        sample_path = os.path.join(DATASET_FOLDER, sample_choice)
        if not os.path.exists(sample_path):
            return jsonify({"success": False, "error": f"Sample file '{sample_choice}' not found."}), 404
        original_filename = sample_choice
        safe_name = f"sample_{sanitize_filename(sample_choice)}"
        saved_image_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
        shutil.copyfile(sample_path, saved_image_path)
        display_image_url = f"/dataset/{sample_choice}"

    else:
        return jsonify({
            "success": False,
            "error": "No image uploaded. Please choose an image file or select a sample image."
        }), 400

    # Validate image file
    is_valid, val_err = validate_image_file(saved_image_path)
    if not is_valid:
        return jsonify({"success": False, "error": val_err}), 400

    # Image Preprocessing
    processed_image_path = saved_image_path
    preprocessed_url = display_image_url

    if use_preprocessing:
        prep_filename = f"prep_{os.path.basename(saved_image_path)}"
        processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], prep_filename)
        try:
            preprocess_image(saved_image_path, save_path=processed_image_path)
            preprocessed_url = f"/uploads/{prep_filename}"
        except Exception as e:
            # Fall back to original image if preprocessing fails
            processed_image_path = saved_image_path

    # OCR Execution
    tesseract_result = None
    gemma_result = None

    if engine in ('tesseract', 'compare'):
        tesseract_result = extract_text_tesseract(processed_image_path)

    if engine in ('gemma', 'compare'):
        gemma_result = extract_text_gemma(processed_image_path)

    return jsonify({
        "success": True,
        "filename": original_filename,
        "engine_selected": engine,
        "preprocessing_used": use_preprocessing,
        "original_image_url": display_image_url,
        "preprocessed_image_url": preprocessed_url,
        "tesseract": tesseract_result,
        "gemma": gemma_result
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"success": False, "error": "File size exceeds maximum upload limit of 10MB."}), 413


@app.errorhandler(500)
def server_error(error):
    return jsonify({"success": False, "error": "An internal server error occurred while processing the request."}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
