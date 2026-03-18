import os
import pytesseract
import cv2
import numpy as np
from PIL import Image

# Configure Tesseract path (Windows users)
# pytesseract.pytesseract.tesseract_cmd = os.getenv(
#    "TESSERACT_CMD",
 #   r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#) 


def extract_text(image_file, language="eng"):
    """
    Extract text from an image using Tesseract OCR.
    Supports English (eng) and Hindi (hin).
    """

    # Step 1: Open image safely
    try:
        image = Image.open(image_file).convert("RGB")
    except Exception:
        raise ValueError("Invalid image file")

    # Step 2: Convert image to NumPy array
    image_np = np.array(image)

    # Step 3: Convert to grayscale
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Step 4: Noise removal (better than Gaussian for OCR)
    gray_image = cv2.medianBlur(gray_image, 3)

    # Step 5: Adaptive thresholding 
    threshold_image = cv2.adaptiveThreshold(
        gray_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Step 6: OCR configuration (improves accuracy)
    custom_config = r'--oem 3 --psm 6'

    # Step 7: Perform OCR
    extracted_text = pytesseract.image_to_string(
        threshold_image,
        lang=language,
        config=custom_config
    )

    # Step 8: Return cleaned text
    return extracted_text.strip()
