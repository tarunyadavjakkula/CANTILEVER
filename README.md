# Cantilever AI Internship Projects

Welcome to the central repository for the **Cantilever AI Internship Program**. This repository houses two independent projects, organized into dedicated subdirectories.

---

## 📁 Repository Overview

| Task / Project | Category | Description | Folder Link |
| :--- | :--- | :--- | :--- |
| **Task 1** | Web Scraping & Data Analysis | Automated E-Commerce Web Scraper, SQLite database storage, statistical analysis, and interactive Flask web dashboard with Chart.js visualizations. | [📁 Task-1-Web-Scraping-Analysis](./Task-1-Web-Scraping-Analysis) |
| **Task 2** | Text Detection & Extraction (OCR) | Multi-engine OCR web system comparing traditional **Tesseract OCR** against local **Gemma / Vision AI** with OpenCV image preprocessing routines. | [📁 Task-2-OCR-Text-Extraction](./Task-2-OCR-Text-Extraction) |

---

## 🚀 Projects Summary

### 1. Task 1: Web Scraping & Data Analysis System
- **Objective**: Collect, clean, analyze, and visualize product data from e-commerce platforms.
- **Key Features**:
  - Web scraping with custom user-agents and retry mechanisms (`scraper.py`).
  - SQLite database persistence with duplicate detection (`database.py`).
  - Automated statistical summary calculations and chart generation (`analysis.py`).
  - Modern Flask web dashboard (`app.py`) for data filtering and inspection.
- **Documentation & Setup**: See [Task 1 README](./Task-1-Web-Scraping-Analysis/README.md).

---

### 2. Task 2: Text Detection and Extraction (OCR) System
- **Objective**: Extract printed and visual text from images using OpenCV preprocessing and dual OCR engines.
- **Key Features**:
  - **OpenCV Preprocessing**: Grayscale conversion, adaptive thresholding (Otsu), upscaling, and noise reduction (`preprocessing.py`).
  - **Tesseract OCR Integration**: Fast, rule-based text extraction with confidence scoring (`ocr.py`).
  - **Gemma Vision AI Integration**: Local LLM/Vision model via Ollama API for structured extraction (`gemma_ocr.py`).
  - **Side-by-Side Comparison UI**: Interactive Flask dashboard for live OCR comparison and image uploads (`app.py`).
  - **Synthetic Test Dataset Generator**: Automated generation of sample receipts, invoices, and notices (`create_dataset.py`).
- **Documentation & Setup**: See [Task 2 README](./Task-2-OCR-Text-Extraction/README.md).

---

## 💻 General Requirements

Each task operates independently and maintains its own `requirements.txt` and virtual environment.

To run any task:
1. Navigate to the task directory:
   ```bash
   cd Task-1-Web-Scraping-Analysis   # For Task 1
   # OR
   cd Task-2-OCR-Text-Extraction    # For Task 2
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate   # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```bash
   python app.py
   ```

---

## 👨‍💻 Author
Developed for the **Cantilever AI Internship**.
