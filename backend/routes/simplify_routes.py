from flask import Blueprint, request, jsonify
from modules.simplifier import simplify_text

# Create Blueprint
simplify_bp = Blueprint("simplify", __name__)


@simplify_bp.route("/process/simplify", methods=["POST"])
def process_simplify():
    """
    API endpoint for text simplification.
    """

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "success": False,
            "error": "No text provided"
        }), 400

    original_text = data["text"]

    simplified = simplify_text(original_text)

    return jsonify({
        "success": True,
        "simplified_text": simplified
    })
