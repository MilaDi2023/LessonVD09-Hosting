from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_login import current_user

from app.models import User # Импортируем модель User из нашего модуля

# Создаём класс RegistrationForm, который будет создавать форму
class RegistrationForm(FlaskForm):
    username = StringField('Логин пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    # Создаём функции для проверки уникальности имени пользователя и почты
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # Ищем в БД первого попавшегося юзера с указанным именем
        if user:
            raise ValidationError('Пользователь с таким логином уже существует.')


# Создание класса LoginForm
class LoginForm(FlaskForm):
    username = StringField('Логин пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

# Создание класса UpdateAccountForm
class UpdateAccountForm(FlaskForm):
    username = StringField('Логин пользователя', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Пароль', validators=[Length(min=6, max=200)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[EqualTo('password')])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Пользователь с таким логином уже существует.')