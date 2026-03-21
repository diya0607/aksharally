import os
import pytesseract
import cv2
import numpy as np
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR"

# Configure Tesseract path (Windows users)
pytesseract.pytesseract.tesseract_cmd = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_text(image_file, language="eng"):
    """
    Extract text from an image using Tesseract OCR.
    Supports English (eng) and Hindi (hin).
    """

    # Open image using Pillow
    image = Image.open(image_file).convert("RGB")

    # Convert image to NumPy array for OpenCV
    image_np = np.array(image)

    # Convert RGB image to Grayscale
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Apply thresholding to improve OCR accuracy
    _, threshold_image = cv2.threshold(
        gray_image, 150, 255, cv2.THRESH_BINARY
    )

    # Perform OCR using Tesseract
    extracted_text = pytesseract.image_to_string(
        threshold_image,
        lang=language
    )

    # Return cleaned text
    return extracted_text.strip()
