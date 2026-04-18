from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from ..extensions import db
from ..forms import LoginForm, RegisterStudentForm, RegisterTeacherForm
from ..models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    return render_template("register_choice.html")


def _handle_registration(form, role: str, role_label: str):
    if form.validate_on_submit():
        existing = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing:
            flash("Пользователь с таким email или логином уже существует", "danger")
            return None

        user = User(username=form.username.data, email=form.email.data, role=role)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f"Регистрация {role_label} успешна. Теперь войдите в аккаунт.", "success")
        return redirect(url_for("auth.login"))

    return None


@auth_bp.route("/register/student", methods=["GET", "POST"])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterStudentForm()
    result = _handle_registration(form, role="student", role_label="ученика")
    if result is not None:
        return result
    return render_template("register.html", form=form, role_name="ученика")


@auth_bp.route("/register/teacher", methods=["GET", "POST"])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterTeacherForm()
    result = _handle_registration(form, role="teacher", role_label="учителя")
    if result is not None:
        return result
    return render_template("register.html", form=form, role_name="учителя")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вы вошли в систему", "success")
            return redirect(url_for("main.dashboard"))

        flash("Неверные email или пароль", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for("main.index"))
