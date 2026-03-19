import os
import pytesseract
import cv2
import numpy as np
from PIL import Image
import easyocr

# Initialize EasyOCR reader (load once)
reader = None

def get_easyocr_reader():
    global reader
    if reader is None:
        print("Loading EasyOCR model...")
        reader = easyocr.Reader(['en'], gpu=False)
    return reader

# (Optional) Set this if needed (Windows users)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image_np):
    """
    Improve image quality for OCR
    """

    # Convert to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Resize (VERY IMPORTANT for accuracy)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Denoise
    gray = cv2.medianBlur(gray, 3)

    # Adaptive threshold (handles uneven lighting)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        15,
        10
    )

    return thresh


def extract_text_easyocr(image_np):
    reader = get_easyocr_reader()
    result = reader.readtext(image_np, detail=0)
    return "\n".join(result)


def extract_text(image_file, language="eng"):
    """
    Extract text using Tesseract with EasyOCR fallback
    """

    # Step 1: Load image safely
    try:
        image = Image.open(image_file).convert("RGB")
    except Exception:
        raise ValueError("Invalid image file")

    image_np = np.array(image)

    # Step 2: Preprocess image
    processed = preprocess_image(image_np)

    # Step 3: Tesseract config
    custom_config = r'--oem 3 --psm 6'

    try:
        # Step 4: Run Tesseract OCR
        text = pytesseract.image_to_string(
            processed,
            lang=language,
            config=custom_config
        )

        # Step 5: Clean & structure output (KEEP line breaks)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        final_text = "\n".join(lines)

        # Remove weird/unprintable characters
        final_text = ''.join(c for c in final_text if c.isprintable())

        # Step 6: Detect bad OCR → fallback
        if len(final_text.split()) < 5:
            raise Exception("Poor OCR output")

        return final_text

    except Exception as e:
        print("Tesseract failed, switching to EasyOCR:", e)

        # Step 7: EasyOCR fallback
        return extract_text_easyocr(processed)