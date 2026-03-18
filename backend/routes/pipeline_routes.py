from flask import Blueprint, request, jsonify
from modules.ocr import extract_text
from modules.simplifier import simplify_text

pipeline_bp = Blueprint("pipeline", __name__)

@pipeline_bp.route("/process/full", methods=["POST"])
def process_full():
    """
    Full pipeline: Image → OCR → Simplify
    """

    # Step 1: Check image
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image file provided"
        }), 400

    try:
        # Step 2: Get image and language
        image = request.files["image"]
        language = request.form.get("language", "eng")

        # Step 3: OCR
        extracted_text = extract_text(image, language)

        # Step 4: Simplify
        simplified_text = simplify_text(extracted_text)

        # Step 5: Return response
        return jsonify({
            "success": True,
            "extracted_text": extracted_text,
            "simplified_text": simplified_text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500