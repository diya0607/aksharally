from flask import Blueprint, request, jsonify
from modules.ocr import extract_text
from modules.simplifier import simplify_text

pipeline_bp = Blueprint("pipeline", __name__)


@pipeline_bp.route("/process/ocr-simplify", methods=["POST"])
def ocr_and_simplify():
    """
    Pipeline API:
    Image → OCR → Text Simplification
    """

    try:
        # 1️⃣ Validate image input
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "error": "No image provided"
            }), 400

        image = request.files["image"]
        language = request.form.get("language", "eng")

        # 2️⃣ Perform OCR
        extracted_text = extract_text(image, language)

        if not extracted_text:
            return jsonify({
                "success": False,
                "error": "No text detected from image"
            }), 400

        # 3️⃣ Simplify extracted text
        simplified_text = simplify_text(extracted_text)

        # 4️⃣ Return final response
        return jsonify({
            "success": True,
            "original_text": extracted_text,
            "simplified_text": simplified_text
        }), 200

    except Exception as e:
        # Catch unexpected errors
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500
