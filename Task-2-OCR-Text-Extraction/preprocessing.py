try:
    import cv2
except ImportError:
    cv2 = None

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os

def read_image_cv2(image_input):
    """Read image from file path or PIL Image to OpenCV BGR format."""
    if cv2 is None:
        raise ImportError("OpenCV (cv2) is not installed. Using PIL fallback.")
    if isinstance(image_input, str):
        img = cv2.imread(image_input)
        if img is None:
            raise ValueError(f"OpenCV could not read image at {image_input}")
        return img
    elif isinstance(image_input, Image.Image):
        # Convert PIL Image to OpenCV numpy array
        return cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
    elif isinstance(image_input, np.ndarray):
        return image_input.copy()
    else:
        raise TypeError("Unsupported image input type")



def convert_to_grayscale(img_bgr):
    """Convert BGR or RGB OpenCV image to 8-bit Grayscale."""
    if len(img_bgr.shape) == 2:
        return img_bgr  # Already grayscale
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)


def resize_image(img_gray, min_width=1200):
    """
    Resize image to ensure sufficient resolution for OCR.
    If image width is smaller than min_width, scale up preserving aspect ratio.
    """
    h, w = img_gray.shape[:2]
    if w >= min_width:
        return img_gray

    scale = min_width / float(w)
    new_w = min_width
    new_h = int(h * scale)
    return cv2.resize(img_gray, (new_w, new_h), interpolation=cv2.INTER_CUBIC)


def denoise_image(img_gray, method='gaussian'):
    """
    Apply noise reduction to remove background specks or scanner grain.
    Supported methods: 'gaussian', 'median', 'bilateral'
    """
    if method == 'gaussian':
        return cv2.GaussianBlur(img_gray, (3, 3), 0)
    elif method == 'median':
        return cv2.medianBlur(img_gray, 3)
    elif method == 'bilateral':
        return cv2.bilateralFilter(img_gray, 9, 75, 75)
    return img_gray


def apply_threshold(img_gray, method='otsu'):
    """
    Binarize/Threshold image to produce high-contrast black text on white background.
    Supported methods: 'otsu', 'adaptive', 'simple'
    """
    if method == 'otsu':
        _, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    elif method == 'adaptive':
        return cv2.adaptiveThreshold(
            img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
    elif method == 'simple':
        _, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
        return thresh
    return img_gray


def preprocess_image(image_input, save_path=None, use_threshold=True, threshold_method='otsu'):
    """
    Complete OpenCV preprocessing pipeline for OCR:
    1. Read Image
    2. Convert to Grayscale
    3. Resize up to threshold width if small
    4. Denoise
    5. Thresholding / Binarization (optional)
    6. Save to disk if save_path is provided.

    Returns preprocessed image as OpenCV array or PIL Image.
    """
    try:
        img_bgr = read_image_cv2(image_input)
        img_gray = convert_to_grayscale(img_bgr)
        img_resized = resize_image(img_gray, min_width=1200)
        img_denoised = denoise_image(img_resized, method='gaussian')

        if use_threshold:
            processed = apply_threshold(img_denoised, method=threshold_method)
        else:
            processed = img_denoised

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            cv2.imwrite(save_path, processed)

        return processed
    except Exception as e:
        # Fallback using PIL if OpenCV encounters any issue
        return _preprocess_pil_fallback(image_input, save_path)


def _preprocess_pil_fallback(image_input, save_path=None):
    """Fallback preprocessing using pure Pillow if OpenCV is unavailable."""
    if isinstance(image_input, str):
        img = Image.open(image_input).convert('L')
    elif isinstance(image_input, Image.Image):
        img = image_input.convert('L')
    elif isinstance(image_input, np.ndarray):
        img = Image.fromarray(image_input).convert('L')
    else:
        raise TypeError("Invalid image input")

    # Resize if small
    w, h = img.size
    if w < 1200:
        scale = 1200 / float(w)
        img = img.resize((1200, int(h * scale)), Image.Resampling.LANCZOS)

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    # Denoise filter
    img = img.filter(ImageFilter.SMOOTH_MORE)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        img.save(save_path)

    return np.array(img)
