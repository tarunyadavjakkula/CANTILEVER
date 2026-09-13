# OCR Text Detection & Extraction

A submission-ready, full-stack web application for Optical Character Recognition (OCR) built using Python, Flask, OpenCV, **Tesseract OCR** (via `pytesseract`), and an optional **Gemma AI Vision** OCR engine.

---

## Overview

This application provides a seamless web interface for uploading images or scanned documents, preprocessing them to optimize image contrast and clarity, and extracting text using traditional pattern-matching OCR (Tesseract) as well as AI-powered Generative Vision models (Gemma).

---

## Objective

The objective of this project is to build an end-to-end OCR pipeline that allows users to:
1. Upload and validate document images (PNG, JPG, JPEG, BMP, TIFF).
2. Preview uploaded images side-by-side with OpenCV preprocessed outputs.
3. Preprocess images using grayscale conversion, resolution scaling, noise reduction, and adaptive thresholding.
4. Extract text using **Tesseract OCR** as the primary required engine.
5. Optionally extract text using **Gemma Vision AI** via local Ollama integration.
6. Compare traditional OCR outputs against AI Vision OCR in real-time.
7. Copy extracted text to clipboard or download it as a clean `.txt` document.
8. Handle unsupported formats, corrupt files, and missing OCR dependencies gracefully.

---

## Technologies Used

- **Language**: Python 3.10+
- **Web Framework**: Flask 3.x
- **OCR Engine**: Tesseract OCR & `pytesseract`
- **AI Vision Engine**: Gemma / PaliGemma / Llama 3.2 Vision via local Ollama API
- **Image Processing**: OpenCV (`cv2`) & Pillow (`PIL`)
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism Dark Theme), JavaScript (ES6+ Clipboard & File Blob APIs)

---

## Features

- 📁 **Multi-Format Image Upload**: Validates file existence, MIME headers, extension, and 10MB size limits.
- 🧪 **Sample Dataset Selection**: Built-in test samples (Invoices, Receipts, Scanned Notices, Small Font, Noisy text).
- 🖼️ **Real-Time Image Preview**: Visual comparison between original and preprocessed images.
- ⚙️ **OpenCV Preprocessing Pipeline**: Grayscale, upscaling, Gaussian noise filtering, and Otsu/Adaptive binarization.
- 🔠 **Tesseract OCR Integration**: Extract text with average confidence score calculation.
- 🤖 **Gemma AI Vision Engine**: Optional local LLM vision inference with zero cloud dependency.
- ⚖️ **Compare Both Mode**: Side-by-side view comparing traditional OCR vs AI Vision OCR.
- 📋 **One-Click Copy & Download**: Copy extracted text to clipboard or export directly as `extracted_text.txt`.
- 🛡️ **Robust Error Handling**: Friendly alert notifications for missing models, bad files, or empty OCR results.

---

## Project Workflow

```
                    IMAGE / DOCUMENT
                           ↓
                     Flask Upload
                           ↓
                   Image Validation
            (File type, Size, PIL check)
                           ↓
                  Image Preprocessing
                   (OpenCV / Pillow)
                           ↓
               ┌───────────┴───────────┐
               ↓                       ↓
         Tesseract OCR             Gemma OCR
         (pytesseract)            (AI Vision)
               ↓                       ↓
               └───────────┬───────────┘
                           ↓
                    Extracted Text
                           ↓
                   Flask Web Interface
                           ↓
             Display / Copy / Download TXT
```

---

## Project Structure

```
task2-ocr/
│
├── app.py                # Main Flask web application, routes, upload & API handlers
├── ocr.py                # Tesseract OCR engine, pytesseract integration & confidence calculation
├── preprocessing.py      # OpenCV image preprocessing (grayscale, resize, denoise, threshold)
├── gemma_ocr.py          # Local Gemma Vision AI engine integration via Ollama API
├── utils.py              # File validation, secure filename generation, text cleaning utilities
├── create_dataset.py     # Generator script for OCR sample dataset images
├── test_ocr.py           # Automated test suite to verify pipeline functionality
├── requirements.txt      # Python dependencies list
├── README.md             # Project documentation and setup guide
├── .gitignore            # Git ignore configuration
│
├── dataset/              # Sample images for testing (invoice, receipt, scanned notice, etc.)
│   ├── sample1_printed_doc.png
│   ├── sample2_scanned_notice.png
│   ├── sample3_invoice.png
│   ├── sample4_receipt.png
│   ├── sample5_small_font.png
│   └── sample6_noisy_text.png
│
├── uploads/              # Uploaded & preprocessed temporary image storage
│   └── .gitkeep
│
├── templates/
│   └── index.html        # Responsive web interface with live preview & compare mode
│
└── static/
    └── style.css         # Modern glassmorphism CSS styling and animations
```

---

## Installation

### 1. Clone & Set Up Python Environment

```bash
cd task2-ocr

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Tesseract Installation Guide

Tesseract OCR engine binary must be installed on your operating system for `pytesseract` to function.

### macOS
Using Homebrew:
```bash
brew install tesseract
```

### Windows
1. Download the installer from [UB-Mannheim Tesseract OCR Wiki](https://github.com/UB-Mannheim/tesseract/wiki).
2. Run the installer (e.g. `tesseract-ocr-w64-setup-v5.x.exe`).
3. Add `C:\Program Files\Tesseract-OCR` to your System Environment Path, or set environment variable:
```cmd
set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev
```

---

## Gemma AI Setup (Optional Feature)

The Gemma AI Vision engine allows testing generative vision models locally using [Ollama](https://ollama.com).

### Enabling Gemma OCR:
1. Download and install Ollama from [ollama.com](https://ollama.com).
2. Start the Ollama daemon:
```bash
ollama serve
```
3. Pull a vision-capable model (such as `paligemma`, `gemma:3b-vision`, or `llama3.2-vision`):
```bash
ollama pull paligemma
# OR
ollama pull llama3.2-vision
```

### Automatic Fallback Behavior:
If Ollama or a vision model is not installed, the application **automatically detects this** and displays:
> *"Gemma OCR is currently unavailable because local Ollama service is not running. Tesseract OCR can still be used."*

Tesseract OCR remains 100% operational regardless of Gemma's availability.

---

## Running the Application

1. Ensure your virtual environment is active and Tesseract is installed.
2. Start the Flask app:

```bash
python app.py
```

3. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## How the OCR Pipeline Works

1. **Upload & Validation**: The file is inspected for valid extension (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`), size limit (<10MB), and image header corruption.
2. **OpenCV Preprocessing**:
   - `convert_to_grayscale`: Removes color artifacts.
   - `resize_image`: Upscales low-resolution text to minimum 1200px width.
   - `denoise_image`: Applies Gaussian filtering to eliminate scanner noise.
   - `apply_threshold`: Applies Otsu's adaptive binarization to produce high-contrast black-and-white text.
3. **Text Extraction**:
   - **Tesseract**: Uses `pytesseract.image_to_string()` and calculates confidence from bounding box word metrics.
   - **Gemma Vision**: Converts image to base64 and prompts the Vision model for structured text extraction without commentary.
4. **Post-Processing & Clean Up**: `clean_ocr_text()` normalizes blank lines while retaining line breaks, numbers, and punctuation.

---

## Tesseract vs Gemma AI Vision Comparison

| Feature | Tesseract OCR | Gemma AI Vision |
| :--- | :--- | :--- |
| **Technology** | Classical Pattern & Feature Recognition | Deep Neural Generative Vision Model |
| **Speed** | Extremely Fast (< 1 sec) | Moderate (depends on local GPU/CPU) |
| **Resource Usage** | Lightweight (MBs of RAM) | High (requires 2GB-4GB VRAM/RAM) |
| **Document Layouts** | Best on clean printed horizontal lines | Strong context understanding & structured key-value parsing |
| **Noisy Images** | Requires preprocessing (binarization) | Resilient to background noise and low contrast |

---

## Preprocessing Impact Analysis

During testing across the sample dataset, we observed that:
- **Clean Printed Text & Invoices**: Tesseract achieves >92% accuracy both with and without preprocessing.
- **Noisy & Low Contrast Scans**: Preprocessing (Gaussian Denoising + Otsu Thresholding) improves Tesseract character detection accuracy significantly by converting faint gray characters into sharp black text.

---

## Testing & Verification

Run the automated test suite to verify all components:

```bash
python test_ocr.py
```

Sample test output:
```
============================================================
RUNNING TASK 2 OCR VERIFICATION SUITE
============================================================
[1] Tesseract Status: Tesseract v5.5.0 is installed and available.
[2] Gemma Status: Gemma OCR is currently unavailable...
[3] Found 6 sample dataset images for OCR testing:

Testing File: sample1_printed_doc.png
  Validation: PASSED
  Preprocessing: OK
  Tesseract OCR: SUCCESS | Confidence: 94.2%
  Extracted Sample: 'CANTILEVER INTERNSHIP TASK 2 Text Detection and Extraction...'
...
```

---

## Limitations

- **OCR Accuracy**: Depends heavily on document resolution, lighting, and blur.
- **Handwriting**: Tesseract standard models are optimized for printed text; handwritten text requires specialized training.
- **Complex Layouts**: Multi-column documents or complex tables may alter reading order in traditional OCR.
- **Hardware Requirements**: Running local Gemma vision models requires sufficient system memory (RAM/VRAM).

---

## Future Improvements

- 📄 Multi-page PDF document upload support.
- 📐 Deep learning document layout & table extraction (e.g. LayoutLM).
- 🌐 Multi-language selection dropdown for Tesseract language packs (`deu`, `fra`, `spa`, `hin`).
- ⚡ Batch processing queue for bulk document folder OCR.
