from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    recaptcha = RecaptchaField()


class RegisterForm(FlaskForm):
    username = StringField("Username")
    email = StringField("Email")
    password = PasswordField("Password")
    recaptcha = RecaptchaField()
    check = BooleanField("isAdmin")

class EventForm(FlaskForm):
    date = StringField("datepicker")
    recaptcha = RecaptchaField()
