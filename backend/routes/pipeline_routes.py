from flask import Blueprint, request, jsonify
from modules.ocr import extract_text
from modules.simplifier import simplify_text

pipeline_bp = Blueprint("pipeline", __name__)


# ✅ MAIN ROUTE (Flutter will use this)
@pipeline_bp.route("/process", methods=["POST"])
def process_full():
    try:
        # Check image
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "error": "No image provided"
            }), 400

        image = request.files["image"]
        language = request.form.get("language", "eng")

        # OCR
        extracted_text = extract_text(image, language)

        if not extracted_text:
            return jsonify({
                "success": False,
                "error": "No text detected from image"
            }), 400

        # Simplify
        simplified_text = simplify_text(extracted_text)

        return jsonify({
            "success": True,
            "original_text": extracted_text,
            "simplified_text": simplified_text
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


# ✅ OPTIONAL ADVANCED ROUTE (same logic)
@pipeline_bp.route("/process/ocr-simplify", methods=["POST"])
def ocr_and_simplify():
    try:
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "error": "No image provided"
            }), 400

        image = request.files["image"]
        language = request.form.get("language", "eng")

        extracted_text = extract_text(image, language)

        if not extracted_text:
            return jsonify({
                "success": False,
                "error": "No text detected from image"
            }), 400

        simplified_text = simplify_text(extracted_text)

        return jsonify({
            "success": True,
            "original_text": extracted_text,
            "simplified_text": simplified_text
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500