from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship("Submission", back_populates="author", cascade="all, delete")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    due_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship("Submission", back_populates="assignment")


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, default=0)
    teacher_comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"), nullable=True)
    assignment = db.relationship("Assignment", back_populates="submissions")

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", back_populates="submissions")
    feedback_messages = db.relationship(
        "FeedbackMessage",
        back_populates="submission",
        cascade="all, delete-orphan",
        order_by="FeedbackMessage.created_at.asc()",
    )

    @property
    def is_submitted_late(self) -> bool:
        if not self.assignment or self.assignment.due_at is None or self.created_at is None:
            return False
        return self.created_at > self.assignment.due_at

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "filename": self.filename,
            "score": self.score,
            "teacher_comment": self.teacher_comment,
            "created_at": self.created_at.isoformat(),
            "author": self.author.username,
            "assignment_id": self.assignment_id,
            "assignment_title": self.assignment.title if self.assignment else None,
            "assignment_due_at": self.assignment.due_at.isoformat()
            if self.assignment and self.assignment.due_at
            else None,
            "submitted_late": self.is_submitted_late,
        }
        return d


class FeedbackMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey("submission.id"), nullable=False)

    sender = db.relationship("User")
    submission = db.relationship("Submission", back_populates="feedback_messages")


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))
