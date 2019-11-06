from wtforms import Form
from wtforms import TextField
from wtforms import PasswordField


class LoginForm(Form):
    username = TextField('username')
    password = PasswordField('password')
