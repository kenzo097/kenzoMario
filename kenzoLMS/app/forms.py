from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import IntegerField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class RegisterForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Подтверждение", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class SubmissionForm(FlaskForm):
    title = StringField("Название работы", validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField("Описание", validators=[DataRequired(), Length(min=10)])
    file = FileField(
        "Файл",
        validators=[
            FileRequired(),
            FileAllowed(["pdf", "docx", "txt", "png", "jpg", "jpeg"], "Недопустимый формат файла"),
        ],
    )
    submit = SubmitField("Отправить работу")


class TeacherScoreForm(FlaskForm):
    score = IntegerField("Балл (0-100)", validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField("Сохранить балл")


class FeedbackMessageForm(FlaskForm):
    body = TextAreaField("Сообщение", validators=[DataRequired(), Length(min=2, max=2000)])
    submit = SubmitField("Отправить")
