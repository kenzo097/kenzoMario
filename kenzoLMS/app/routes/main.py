import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from functools import wraps

from flask import Blueprint, Response, current_app, flash, redirect, render_template, send_from_directory, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

from ..extensions import db
from ..forms import AssignmentForm, FeedbackMessageForm, SubmissionForm, TeacherScoreForm
from ..models import Assignment, FeedbackMessage, Submission


main_bp = Blueprint("main", __name__)


def is_teacher(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    if getattr(user, "role", "student") == "teacher":
        return True
    email = (user.email or "").lower()
    teacher_emails = {item.lower() for item in current_app.config.get("TEACHER_EMAILS", [])}
    return "teacher" in email or email in teacher_emails


def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not is_teacher(current_user):
            flash("Доступно только преподавателю", "danger")
            return redirect(url_for("main.dashboard"))
        return view_func(*args, **kwargs)

    return wrapper


def _submission_assignment_choices():
    rows = Assignment.query.order_by(Assignment.created_at.desc()).all()
    choices = [(0, "— Без задания (произвольная работа) —")]
    for a in rows:
        if a.due_at:
            label = f"{a.title} — срок {a.due_at.strftime('%d.%m.%Y %H:%M')}"
        else:
            label = f"{a.title} (без дедлайна)"
        choices.append((a.id, label))
    return choices


def _brand_icon_response():
    return send_from_directory(
        current_app.static_folder,
        "img/logo-kenzo-brand.png",
        mimetype="image/png",
    )


@main_bp.get("/favicon.ico")
def favicon():
    return _brand_icon_response()


@main_bp.get("/apple-touch-icon.png")
@main_bp.get("/apple-touch-icon-precomposed.png")
def apple_touch_icon():
    return _brand_icon_response()


@main_bp.route("/")
def index():
    latest = Submission.query.order_by(Submission.created_at.desc()).limit(5).all()
    return render_template("index.html", latest=latest)


@main_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = SubmissionForm()
    form.assignment_id.choices = _submission_assignment_choices()
    if form.validate_on_submit():
        aid = form.assignment_id.data
        if aid and Assignment.query.get(aid) is None:
            flash("Выбранное задание не найдено", "danger")
            return redirect(url_for("main.dashboard"))

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
            assignment_id=aid if aid else None,
        )

        db.session.add(submission)
        db.session.commit()

        flash("Работа загружена", "success")
        return redirect(url_for("main.dashboard"))

    items = (
        Submission.query.options(joinedload(Submission.assignment))
        .filter_by(author_id=current_user.id)
        .order_by(Submission.created_at.desc())
        .all()
    )
    return render_template("dashboard.html", form=form, items=items)


@main_bp.route("/files/<path:filename>")
@login_required
def uploaded_file(filename: str):
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, filename, as_attachment=True)


@main_bp.route("/teacher/assignments", methods=["GET", "POST"])
@login_required
@teacher_required
def teacher_assignments():
    form = AssignmentForm()
    if form.validate_on_submit():
        instructions = (form.instructions.data or "").strip() or None
        row = Assignment(
            title=form.title.data.strip(),
            instructions=instructions,
            due_at=form.due_at.data,
        )
        db.session.add(row)
        db.session.commit()
        flash("Задание создано", "success")
        return redirect(url_for("main.teacher_assignments"))

    items = Assignment.query.order_by(Assignment.created_at.desc()).all()
    return render_template("teacher_assignments.html", form=form, items=items)


@main_bp.route("/teacher/review", methods=["GET"])
@login_required
@teacher_required
def teacher_review():
    items = (
        Submission.query.options(joinedload(Submission.assignment))
        .order_by(Submission.created_at.desc())
        .all()
    )
    form = TeacherScoreForm()
    return render_template("teacher_review.html", items=items, form=form)


@main_bp.get("/teacher/review/export.csv")
@login_required
@teacher_required
def teacher_review_export_csv():
    items = (
        Submission.query.options(joinedload(Submission.assignment))
        .order_by(Submission.created_at.desc())
        .all()
    )
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "id",
            "title",
            "description",
            "filename",
            "author_username",
            "author_email",
            "score",
            "teacher_comment",
            "created_at",
            "assignment_id",
            "assignment_title",
            "assignment_due_at",
            "submitted_late",
        ]
    )
    for s in items:
        writer.writerow(
            [
                s.id,
                s.title,
                s.description or "",
                s.filename,
                s.author.username,
                s.author.email,
                s.score,
                s.teacher_comment or "",
                s.created_at.strftime("%Y-%m-%d %H:%M:%S") if s.created_at else "",
                s.assignment_id or "",
                s.assignment.title if s.assignment else "",
                s.assignment.due_at.strftime("%Y-%m-%d %H:%M:%S")
                if s.assignment and s.assignment.due_at
                else "",
                "yes" if s.is_submitted_late else "no",
            ]
        )
    filename = f"submissions_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.csv"
    return Response(
        buffer.getvalue().encode("utf-8-sig"),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@main_bp.route("/teacher/review/<int:submission_id>/score", methods=["POST"])
@login_required
@teacher_required
def set_score(submission_id: int):
    form = TeacherScoreForm()
    if form.validate_on_submit():
        item = Submission.query.get_or_404(submission_id)
        item.score = form.score.data
        comment = (form.teacher_comment.data or "").strip()
        item.teacher_comment = comment if comment else None
        db.session.commit()
        flash("Балл и комментарий сохранены", "success")
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
