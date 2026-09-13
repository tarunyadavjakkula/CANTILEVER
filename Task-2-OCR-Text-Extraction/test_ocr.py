import os
import sys

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import validate_image_file, clean_ocr_text
from preprocessing import preprocess_image
from ocr import is_tesseract_available, extract_text_tesseract
from gemma_ocr import check_gemma_availability, extract_text_gemma

DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")


def run_tests():
    print("=" * 60)
    print("RUNNING TASK 2 OCR VERIFICATION SUITE")
    print("=" * 60)

    # 1. System availability check
    tess_ok, tess_msg = is_tesseract_available()
    print(f"\n[1] Tesseract Status: {tess_msg}")

    gemma_ok, gemma_model, gemma_msg = check_gemma_availability()
    print(f"[2] Gemma Status: {gemma_msg}")

    # 2. Test Dataset Processing
    sample_files = [f for f in os.listdir(DATASET_DIR) if f.endswith(".png")]
    print(f"\n[3] Found {len(sample_files)} sample dataset images for OCR testing:\n")

    for sample in sorted(sample_files):
        sample_path = os.path.join(DATASET_DIR, sample)
        print("-" * 50)
        print(f"Testing File: {sample}")

        # Validation
        valid, err = validate_image_file(sample_path)
        print(f"  Validation: {'PASSED' if valid else 'FAILED (' + str(err) + ')'}")
        if not valid:
            continue

        # Preprocessing
        prep_path = os.path.join(DATASET_DIR, f"prep_test_{sample}")
        try:
            preprocess_image(sample_path, save_path=prep_path)
            print(f"  Preprocessing: OK (saved prep_test_{sample})")
        except Exception as e:
            print(f"  Preprocessing Failed: {e}")

        # Tesseract OCR
        tess_res = extract_text_tesseract(prep_path if os.path.exists(prep_path) else sample_path)
        if tess_res.get("success"):
            text_snippet = tess_res.get("text", "").replace("\n", " ")[:90]
            conf = tess_res.get("confidence")
            conf_str = f"{conf}%" if conf is not None else "N/A"
            print(f"  Tesseract OCR: SUCCESS | Confidence: {conf_str}")
            print(f"  Extracted Sample: '{text_snippet}...'\n")
        else:
            print(f"  Tesseract OCR: FAILED | Error: {tess_res.get('error')}\n")

        # Cleanup test prep file
        if os.path.exists(prep_path):
            os.remove(prep_path)

    print("=" * 60)
    print("VERIFICATION SUITE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
