from flask import Blueprint, request, jsonify
from modules.ocr import extract_text

# Create Blueprint for OCR routes
ocr_bp = Blueprint("ocr", __name__)

@ocr_bp.route("/process/ocr", methods=["POST"])
def process_ocr():
    """
    API endpoint to process OCR from uploaded image.
    """

    # Validate image input
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image file provided"
        }), 400

    # Get image and language
    image = request.files["image"]
    language = request.form.get("language", "eng")

    # Extract text using OCR module
    extracted_text = extract_text(image, language)

    # Return response
    return jsonify({
        "success": True,
        "extracted_text": extracted_text
    })
