import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def get_font(size):
    """Attempt to load standard system font or default font."""
    font_names = [
        "DejaVuSans.ttf", "Arial.ttf", "Helvetica.ttf", "LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def create_printed_doc(output_path):
    """Sample 1: Clean Printed Document"""
    img = Image.new("RGB", (1000, 1200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    title_font = get_font(32)
    heading_font = get_font(24)
    body_font = get_font(18)

    draw.text((80, 80), "CANTILEVER INTERNSHIP TASK 2", fill=(20, 30, 70), font=title_font)
    draw.text((80, 130), "Text Detection and Extraction (OCR) Report", fill=(60, 60, 60), font=heading_font)
    draw.line([(80, 170), (920, 170)], fill=(200, 200, 200), width=2)

    lines = [
        "Date: September 8, 2026",
        "Author: Computer Vision & AI Research Team",
        "",
        "1. Executive Summary",
        "Optical Character Recognition (OCR) enables automated extraction of printed",
        "and handwritten text from digital images and scanned documents.",
        "",
        "2. Technical Approach",
        "- Preprocessing: OpenCV Grayscale, Denoising, and Adaptive Thresholding.",
        "- Primary OCR Engine: Tesseract OCR via pytesseract API.",
        "- Secondary AI Engine: Gemma AI Vision model for structured document parsing.",
        "",
        "3. Key System Features",
        "1. High accuracy text detection across variable font sizes.",
        "2. Real-time side-by-side comparison of traditional vs AI OCR.",
        "3. Export options: One-click Clipboard Copy and TXT Download."
    ]

    y = 200
    for line in lines:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            draw.text((80, y), line, fill=(30, 30, 30), font=heading_font)
            y += 40
        else:
            draw.text((80, y), line, fill=(40, 40, 40), font=body_font)
            y += 30

    img.save(output_path)
    print(f"Created {output_path}")


def create_scanned_notice(output_path):
    """Sample 2: Scanned Official Notice with Noise"""
    img = Image.new("RGB", (1000, 1100), color=(248, 246, 240))
    draw = ImageDraw.Draw(img)

    font_large = get_font(28)
    font_med = get_font(20)
    font_small = get_font(16)

    draw.text((250, 70), "NATIONAL INSTITUTE OF TECHNOLOGY", fill=(0, 51, 102), font=font_large)
    draw.text((360, 115), "OFFICIAL ANNOUNCEMENT", fill=(150, 0, 0), font=font_med)
    draw.text((80, 170), "Ref No: NIT/REG/2026/OCR-892", fill=(50, 50, 50), font=font_small)
    draw.text((750, 170), "Date: 08-09-2026", fill=(50, 50, 50), font=font_small)
    draw.line([(80, 200), (920, 200)], fill=(100, 100, 100), width=2)

    lines = [
        "SUBJECT: SUBMISSION DEADLINE FOR TASK 2 OCR PROJECT",
        "",
        "All candidates participating in the CantiLever AI Internship program are hereby",
        "notified that Task 2 (Text Detection & Extraction) must be submitted by 23:59 IST.",
        "",
        "Important Guidelines:",
        "1. Ensure Tesseract OCR engine is properly linked using pytesseract.",
        "2. Include OpenCV image preprocessing routines (grayscale & thresholding).",
        "3. Provide optional Gemma AI Vision engine integration.",
        "4. Validate file uploads and handle errors gracefully.",
        "",
        "By Order of the Academic Registrar,"
    ]

    y = 230
    for line in lines:
        if line.startswith("SUBJECT"):
            draw.text((80, y), line, fill=(0, 0, 0), font=font_med)
            y += 45
        else:
            draw.text((80, y), line, fill=(30, 30, 30), font=font_small)
            y += 32

    draw.text((80, y + 40), "Registrar Office Seal", fill=(100, 100, 100), font=font_small)

    img.save(output_path)
    print(f"Created {output_path}")


def create_invoice(output_path):
    """Sample 3: Commercial Invoice"""
    img = Image.new("RGB", (1000, 1100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_title = get_font(36)
    font_bold = get_font(20)
    font_regular = get_font(16)

    draw.text((70, 60), "CANTILEVER TECH LABS", fill=(30, 80, 180), font=font_title)
    draw.text((70, 110), "123 Innovation Way, Tech Park, Suite 400", fill=(100, 100, 100), font=font_regular)
    draw.text((70, 135), "Email: contact@cantilevertech.org", fill=(100, 100, 100), font=font_regular)

    draw.text((700, 60), "INVOICE", fill=(40, 40, 40), font=font_title)
    draw.text((700, 110), "Invoice #: INV-2026-042", fill=(60, 60, 60), font=font_regular)
    draw.text((700, 135), "Date: Sept 08, 2026", fill=(60, 60, 60), font=font_regular)

    draw.line([(70, 180), (930, 180)], fill=(220, 220, 220), width=2)

    draw.text((70, 200), "Billed To:", fill=(0, 0, 0), font=font_bold)
    draw.text((70, 230), "Acme Solutions Corp", fill=(50, 50, 50), font=font_regular)
    draw.text((70, 255), "Attn: Engineering Department", fill=(50, 50, 50), font=font_regular)

    # Table Header
    draw.rectangle([(70, 310), (930, 350)], fill=(240, 242, 245))
    draw.text((90, 320), "Description", fill=(0, 0, 0), font=font_bold)
    draw.text((500, 320), "Qty", fill=(0, 0, 0), font=font_bold)
    draw.text((650, 320), "Unit Price", fill=(0, 0, 0), font=font_bold)
    draw.text((820, 320), "Total", fill=(0, 0, 0), font=font_bold)

    items = [
        ("OCR Software Module Development", "1", "$450.00", "$450.00"),
        ("OpenCV Preprocessing Optimization", "2", "$125.00", "$250.00"),
        ("Gemma AI Vision Integration", "1", "$300.00", "$300.00"),
        ("Flask API & Web Interface", "1", "$200.00", "$200.00")
    ]

    y = 370
    for desc, qty, price, total in items:
        draw.text((90, y), desc, fill=(40, 40, 40), font=font_regular)
        draw.text((500, y), qty, fill=(40, 40, 40), font=font_regular)
        draw.text((650, y), price, fill=(40, 40, 40), font=font_regular)
        draw.text((820, y), total, fill=(40, 40, 40), font=font_regular)
        draw.line([(70, y + 35), (930, y + 35)], fill=(240, 240, 240), width=1)
        y += 45

    draw.text((650, y + 20), "Subtotal:", fill=(0, 0, 0), font=font_bold)
    draw.text((820, y + 20), "$1200.00", fill=(0, 0, 0), font=font_bold)

    draw.text((650, y + 50), "Tax (10%):", fill=(0, 0, 0), font=font_bold)
    draw.text((820, y + 50), "$120.00", fill=(0, 0, 0), font=font_bold)

    draw.line([(650, y + 85), (930, y + 85)], fill=(0, 0, 0), width=2)
    draw.text((650, y + 95), "Total Due:", fill=(180, 0, 0), font=font_bold)
    draw.text((820, y + 95), "$1320.00", fill=(180, 0, 0), font=font_bold)

    img.save(output_path)
    print(f"Created {output_path}")


def create_receipt(output_path):
    """Sample 4: Supermarket Receipt"""
    img = Image.new("RGB", (600, 900), color=(252, 252, 250))
    draw = ImageDraw.Draw(img)

    font_header = get_font(26)
    font_regular = get_font(18)
    font_bold = get_font(18)

    draw.text((150, 40), "SUPERMARKET EXPRESS", fill=(0, 0, 0), font=font_header)
    draw.text((190, 75), "Store #402 - Main St", fill=(80, 80, 80), font=font_regular)
    draw.text((210, 105), "Tel: 555-0199", fill=(80, 80, 80), font=font_regular)
    draw.text((60, 140), "- - - - - - - - - - - - - - - - - - - - - - - - -", fill=(150, 150, 150), font=font_regular)

    items = [
        ("Organic Milk 1L", "2 x $3.49", "$6.98"),
        ("Whole Wheat Bread", "1 x $2.99", "$2.99"),
        ("Fresh Bananas 1kg", "1 x $1.89", "$1.89"),
        ("Dark Chocolate 100g", "3 x $2.50", "$7.50"),
        ("Green Tea Box", "1 x $4.25", "$4.25")
    ]

    y = 170
    for name, qty_str, price in items:
        draw.text((60, y), name, fill=(20, 20, 20), font=font_regular)
        draw.text((470, y), price, fill=(20, 20, 20), font=font_regular)
        draw.text((80, y + 25), qty_str, fill=(100, 100, 100), font=get_font(14))
        y += 55

    draw.text((60, y), "- - - - - - - - - - - - - - - - - - - - - - - - -", fill=(150, 150, 150), font=font_regular)
    y += 30

    draw.text((60, y), "Subtotal", fill=(0, 0, 0), font=font_regular)
    draw.text((470, y), "$23.61", fill=(0, 0, 0), font=font_regular)

    draw.text((60, y + 30), "Sales Tax (8%)", fill=(0, 0, 0), font=font_regular)
    draw.text((470, y + 30), "$1.89", fill=(0, 0, 0), font=font_regular)

    draw.text((60, y + 70), "TOTAL PAID", fill=(0, 0, 0), font=font_bold)
    draw.text((470, y + 70), "$25.50", fill=(0, 0, 0), font=font_bold)

    draw.text((140, y + 130), "THANK YOU FOR SHOPPING!", fill=(60, 60, 60), font=font_regular)
    draw.text((180, y + 165), "08/09/2026 14:32:05", fill=(100, 100, 100), font=get_font(14))

    img.save(output_path)
    print(f"Created {output_path}")


def create_small_font_terms(output_path):
    """Sample 5: Small Font Document with Terms"""
    img = Image.new("RGB", (900, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_title = get_font(24)
    font_small = get_font(13)

    draw.text((60, 50), "TERMS AND CONDITIONS OF SERVICE", fill=(0, 0, 0), font=font_title)
    draw.line([(60, 85), (840, 85)], fill=(180, 180, 180), width=1)

    terms = [
        "1. Acceptance of Terms: By accessing and using this OCR application, you agree to comply with all terms.",
        "2. User Data Privacy: Uploaded document images are processed locally on server instances and are not sold.",
        "3. Limitation of Liability: CantiLever Tech Labs shall not be liable for OCR misreadings or errors.",
        "4. Intellectual Property: All software algorithms, code structures, and user interface designs remain protected.",
        "5. Governing Law: These terms shall be governed by and construed in accordance with standard regulations.",
        "6. Contact Information: For support or inquiries, please contact support@cantilever.org or call 1-800-OCR-LABS."
    ]

    y = 110
    for term in terms:
        draw.text((60, y), term, fill=(50, 50, 50), font=font_small)
        y += 30

    img.save(output_path)
    print(f"Created {output_path}")


def create_noisy_text(output_path):
    """Sample 6: Noisy Document for Preprocessing Testing"""
    img = Image.new("RGB", (900, 800), color=(235, 235, 225))
    draw = ImageDraw.Draw(img)

    font_header = get_font(28)
    font_body = get_font(20)

    draw.text((100, 60), "WARNING: HIGH VOLTAGE AREA", fill=(180, 0, 0), font=font_header)
    draw.text((100, 120), "Authorized Personnel Only Beyond This Point", fill=(30, 30, 30), font=font_body)
    draw.text((100, 170), "Safety helmets and protective gear mandatory.", fill=(30, 30, 30), font=font_body)
    draw.text((100, 220), "Emergency Contact: Extension 4099", fill=(30, 30, 30), font=font_body)

    # Convert to numpy array to add synthetic noise grain
    arr = np.array(img)
    noise = np.random.normal(0, 25, arr.shape).astype(np.int16)
    noisy_arr = np.clip(arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    noisy_img = Image.fromarray(noisy_arr)
    noisy_img.save(output_path)
    print(f"Created {output_path}")


def generate_all_samples():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, "dataset")
    os.makedirs(dataset_dir, exist_ok=True)

    create_printed_doc(os.path.join(dataset_dir, "sample1_printed_doc.png"))
    create_scanned_notice(os.path.join(dataset_dir, "sample2_scanned_notice.png"))
    create_invoice(os.path.join(dataset_dir, "sample3_invoice.png"))
    create_receipt(os.path.join(dataset_dir, "sample4_receipt.png"))
    create_small_font_terms(os.path.join(dataset_dir, "sample5_small_font.png"))
    create_noisy_text(os.path.join(dataset_dir, "sample6_noisy_text.png"))


if __name__ == "__main__":
    generate_all_samples()
