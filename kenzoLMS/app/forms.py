from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import DateTimeLocalField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


class RegisterForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Подтверждение", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Зарегистрироваться")


class RegisterStudentForm(RegisterForm):
    submit = SubmitField("Зарегистрироваться как ученик")


class RegisterTeacherForm(RegisterForm):
    submit = SubmitField("Зарегистрироваться как учитель")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class SubmissionForm(FlaskForm):
    assignment_id = SelectField(
        "Задание",
        coerce=int,
        choices=[(0, "— Без задания (произвольная работа) —")],
    )
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


class AssignmentForm(FlaskForm):
    title = StringField("Название задания", validators=[DataRequired(), Length(min=2, max=150)])
    instructions = TextAreaField("Условия (необязательно)", validators=[Optional(), Length(max=4000)])
    due_at = DateTimeLocalField("Срок сдачи", validators=[Optional()])
    submit = SubmitField("Создать задание")


class TeacherScoreForm(FlaskForm):
    score = IntegerField("Балл (0-100)", validators=[DataRequired(), NumberRange(min=0, max=100)])
    teacher_comment = TextAreaField(
        "Комментарий к оценке",
        validators=[Optional(), Length(max=2000)],
    )
    submit = SubmitField("Сохранить балл")


class FeedbackMessageForm(FlaskForm):
    body = TextAreaField("Сообщение", validators=[DataRequired(), Length(min=2, max=2000)])
    submit = SubmitField("Отправить")
