import os
import base64
import requests
from utils import clean_ocr_text

OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
# Priority list of vision-capable models supported by Ollama / Gemma AI vision runtimes
PREFERRED_VISION_MODELS = [
    "paligemma",
    "gemma:3b-vision",
    "gemma2:vision",
    "llama3.2-vision",
    "llava",
    "moondream",
    "gemma:2b"
]


def check_gemma_availability():
    """
    Check if Ollama server is running and determine available vision model.
    Returns (is_available: bool, model_name: str or None, message: str).
    """
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/api/tags", timeout=3)
        if response.status_code != 200:
            return False, None, "Ollama service returned non-200 status code."

        data = response.json()
        installed_models = [m.get("name", "") for m in data.get("models", [])]

        if not installed_models:
            return False, None, "Ollama service running, but no local models are installed."

        # Check for matching vision models
        for preferred in PREFERRED_VISION_MODELS:
            for installed in installed_models:
                if preferred in installed.lower():
                    return True, installed, f"Gemma/Vision model '{installed}' is available."

        # If ollama is running but no explicit vision model is pulled yet
        return False, None, (
            "Gemma OCR is currently unavailable because no local Vision AI model "
            "(e.g., paligemma, llama3.2-vision, llava) was found in Ollama. "
            "Tesseract OCR can still be used."
        )

    except requests.exceptions.RequestException:
        return False, None, (
            "Gemma OCR is currently unavailable because local Ollama service is not running. "
            "Tesseract OCR can still be used."
        )


def _encode_image_base64(image_input):
    """Convert file path or image bytes to base64 string."""
    if isinstance(image_input, str):
        with open(image_input, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    elif isinstance(image_input, bytes):
        return base64.b64encode(image_input).decode("utf-8")
    else:
        raise TypeError("Image input must be file path or bytes")


def extract_text_gemma(image_input, model_name=None):
    """
    Extract text using local Gemma Vision AI model via Ollama API.

    Prompting instructions:
    - Read visible text in image.
    - Preserve line breaks, numbers, punctuation.
    - Avoid explanations or hallucinated text.
    - Return ONLY detected text.
    """
    is_avail, detected_model, avail_msg = check_gemma_availability()

    if not is_avail:
        return {
            "success": False,
            "engine": "Gemma OCR",
            "text": "",
            "error": avail_msg
        }

    target_model = model_name or detected_model

    ocr_prompt = (
        "You are an expert Optical Character Recognition (OCR) system. "
        "Task: Read and extract all visible text from this image accurately. "
        "Rules:\n"
        "1. Extract ONLY the text printed or written in the image.\n"
        "2. Preserve original line breaks, numbers, spelling, and punctuation.\n"
        "3. Do NOT add any explanations, introductory text, markdown commentary, or quotes.\n"
        "4. If no text is visible, respond with: 'No readable text was detected.'"
    )

    try:
        img_base64 = _encode_image_base64(image_input)

        payload = {
            "model": target_model,
            "prompt": ocr_prompt,
            "images": [img_base64],
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for deterministic OCR
                "top_p": 0.9
            }
        }

        resp = requests.post(f"{OLLAMA_API_BASE}/api/generate", json=payload, timeout=45)

        if resp.status_code == 200:
            result = resp.json()
            raw_response = result.get("response", "")
            cleaned_response = clean_ocr_text(raw_response)

            return {
                "success": True,
                "engine": f"Gemma OCR ({target_model})",
                "text": cleaned_response or "No readable text detected.",
                "error": None
            }
        else:
            return {
                "success": False,
                "engine": "Gemma OCR",
                "text": "",
                "error": f"Ollama API returned HTTP status {resp.status_code}: {resp.text}"
            }

    except Exception as e:
        return {
            "success": False,
            "engine": "Gemma OCR",
            "text": "",
            "error": f"Gemma Vision OCR execution error: {str(e)}"
        }
