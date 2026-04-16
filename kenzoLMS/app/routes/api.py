from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import Submission


api_bp = Blueprint("api", __name__)


@api_bp.get("/submissions")
def get_submissions():
    items = Submission.query.order_by(Submission.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])


@api_bp.get("/submissions/<int:item_id>")
def get_submission(item_id: int):
    item = Submission.query.get_or_404(item_id)
    return jsonify(item.to_dict())


@api_bp.post("/submissions/<int:item_id>/score")
def rate_submission(item_id: int):
    item = Submission.query.get_or_404(item_id)
    payload = request.get_json(silent=True) or {}
    score = payload.get("score")

    if not isinstance(score, int) or not 0 <= score <= 100:
        return jsonify({"error": "score должен быть целым числом от 0 до 100"}), 400

    item.score = score
    db.session.commit()
    return jsonify(item.to_dict())
