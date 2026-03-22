from flask import Blueprint, request, jsonify
from modules.simplifier import process_text
from modules.ocr import extract_text
import numpy as np
import cv2

pipeline_bp = Blueprint("pipeline", __name__)


@pipeline_bp.route("/process/ocr-format", methods=["POST"])
def ocr_and_format():
    try:
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "error": "No image provided"
            }), 400

        image_file = request.files["image"]
        image_bytes = image_file.read()

        if not image_bytes:
            return jsonify({
                "success": False,
                "error": "Empty image file"
            }), 400

        np_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({
                "success": False,
                "error": "Invalid image format"
            }), 400

        extracted_text = extract_text(image)

        if not extracted_text:
            return jsonify({
                "success": False,
                "error": "No text detected"
            }), 400

        formatted_text = process_text(extracted_text)

        return jsonify({
            "success": True,
            "original_text": extracted_text,
            "formatted_text": formatted_text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500