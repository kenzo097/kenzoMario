from pathlib import Path
from uuid import uuid4

from functools import wraps

from flask import Blueprint, current_app, flash, redirect, render_template, send_from_directory, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ..extensions import db
from ..forms import FeedbackMessageForm, SubmissionForm, TeacherScoreForm
from ..models import FeedbackMessage, Submission


main_bp = Blueprint("main", __name__)


def is_teacher(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    return user.email in current_app.config.get("TEACHER_EMAILS", [])


def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not is_teacher(current_user):
            flash("Доступно только преподавателю", "danger")
            return redirect(url_for("main.dashboard"))
        return view_func(*args, **kwargs)

    return wrapper


@main_bp.route("/")
def index():
    latest = Submission.query.order_by(Submission.created_at.desc()).limit(5).all()
    return render_template("index.html", latest=latest)


@main_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = SubmissionForm()
    if form.validate_on_submit():
        upload = form.file.data
        safe_name = secure_filename(upload.filename)
        unique_name = f"{uuid4().hex}_{safe_name}"

        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        file_path = upload_folder / unique_name
        upload.save(file_path)

        submission = Submission(
            title=form.title.data,
            description=form.description.data,
            filename=unique_name,
            author=current_user,
        )

        db.session.add(submission)
        db.session.commit()

        flash("Работа загружена", "success")
        return redirect(url_for("main.dashboard"))

    items = Submission.query.filter_by(author_id=current_user.id).order_by(Submission.created_at.desc()).all()
    return render_template("dashboard.html", form=form, items=items)


@main_bp.route("/files/<path:filename>")
@login_required
def uploaded_file(filename: str):
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, filename, as_attachment=True)


@main_bp.route("/teacher/review", methods=["GET"])
@login_required
@teacher_required
def teacher_review():
    items = Submission.query.order_by(Submission.created_at.desc()).all()
    form = TeacherScoreForm()
    return render_template("teacher_review.html", items=items, form=form)


@main_bp.route("/teacher/review/<int:submission_id>/score", methods=["POST"])
@login_required
@teacher_required
def set_score(submission_id: int):
    form = TeacherScoreForm()
    if form.validate_on_submit():
        item = Submission.query.get_or_404(submission_id)
        item.score = form.score.data
        db.session.commit()
        flash("Балл обновлён", "success")
    else:
        flash("Введите корректный балл от 0 до 100", "danger")

    return redirect(url_for("main.teacher_review"))


@main_bp.route("/feedback/<int:submission_id>", methods=["GET", "POST"])
@login_required
def feedback_chat(submission_id: int):
    submission = Submission.query.get_or_404(submission_id)
    can_access = is_teacher(current_user) or submission.author_id == current_user.id
    if not can_access:
        flash("У вас нет доступа к этому чату", "danger")
        return redirect(url_for("main.dashboard"))

    form = FeedbackMessageForm()
    if form.validate_on_submit():
        message = FeedbackMessage(
            body=form.body.data.strip(),
            sender_id=current_user.id,
            submission_id=submission.id,
        )
        db.session.add(message)
        db.session.commit()
        flash("Сообщение отправлено", "success")
        return redirect(url_for("main.feedback_chat", submission_id=submission.id))

    messages = submission.feedback_messages
    return render_template(
        "feedback_chat.html",
        submission=submission,
        form=form,
        messages=messages,
        is_teacher_user=is_teacher(current_user),
    )
