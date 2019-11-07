from wtforms import Form
from wtforms import TextField
from wtforms import PasswordField


class LoginForm(Form):
    email = TextField('email')
    password = PasswordField('password')
