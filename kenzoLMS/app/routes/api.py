from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from ..extensions import db
from ..models import Submission


api_bp = Blueprint("api", __name__)


@api_bp.get("/submissions")
def get_submissions():
    items = (
        Submission.query.options(joinedload(Submission.assignment))
        .order_by(Submission.created_at.desc())
        .all()
    )
    return jsonify([item.to_dict() for item in items])


@api_bp.get("/submissions/<int:item_id>")
def get_submission(item_id: int):
    item = Submission.query.options(joinedload(Submission.assignment)).get_or_404(item_id)
    return jsonify(item.to_dict())


@api_bp.post("/submissions/<int:item_id>/score")
def rate_submission(item_id: int):
    item = Submission.query.options(joinedload(Submission.assignment)).get_or_404(item_id)
    payload = request.get_json(silent=True) or {}
    score = payload.get("score")

    if not isinstance(score, int) or not 0 <= score <= 100:
        return jsonify({"error": "score должен быть целым числом от 0 до 100"}), 400

    if "teacher_comment" in payload:
        teacher_comment = payload["teacher_comment"]
        if teacher_comment is None:
            item.teacher_comment = None
        elif not isinstance(teacher_comment, str):
            return jsonify({"error": "teacher_comment должен быть строкой или null"}), 400
        elif len(teacher_comment) > 2000:
            return jsonify({"error": "teacher_comment не длиннее 2000 символов"}), 400
        else:
            comment = teacher_comment.strip()
            item.teacher_comment = comment if comment else None

    item.score = score
    db.session.commit()
    return jsonify(item.to_dict())
