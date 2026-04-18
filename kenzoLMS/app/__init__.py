from pathlib import Path

from flask import Flask
from sqlalchemy import text

from .extensions import db, login_manager
from .routes.auth import auth_bp
from .routes.main import main_bp
from .routes.api import api_bp


def ensure_user_role_column() -> None:
    columns = db.session.execute(text("PRAGMA table_info(user)")).fetchall()
    column_names = {column[1] for column in columns}
    if "role" not in column_names:
        db.session.execute(text("ALTER TABLE user ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'student'"))
        db.session.commit()


def ensure_submission_teacher_comment_column() -> None:
    columns = db.session.execute(text("PRAGMA table_info(submission)")).fetchall()
    column_names = {column[1] for column in columns}
    if "teacher_comment" not in column_names:
        db.session.execute(text("ALTER TABLE submission ADD COLUMN teacher_comment TEXT"))
        db.session.commit()


def ensure_submission_assignment_id_column() -> None:
    columns = db.session.execute(text("PRAGMA table_info(submission)")).fetchall()
    column_names = {column[1] for column in columns}
    if "assignment_id" not in column_names:
        db.session.execute(text("ALTER TABLE submission ADD COLUMN assignment_id INTEGER"))
        db.session.commit()


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.update(
        SECRET_KEY="change-me-in-production",
        SQLALCHEMY_DATABASE_URI="sqlite:///lms.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=str(Path(__file__).resolve().parent / "static" / "uploads"),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,
        TEACHER_EMAILS=["teacher@example.com"],
    )

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()
        ensure_user_role_column()
        ensure_submission_teacher_comment_column()
        ensure_submission_assignment_id_column()

    return app
