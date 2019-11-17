from wtforms import Form
from wtforms import TextField
from wtforms import DateField
from wtforms import PasswordField
from wtforms import SelectField


class LoginForm(Form):
    """Login form for creation/edition access."""

    email = TextField('email')
    password = PasswordField('password')


class UserForm(Form):
    """User form for creation/edition."""

    name = TextField('name')
    first_last_name = TextField('first_last_name')
    second_last_name = TextField('second_last_name')
    email = TextField('email')
    password = PasswordField('password')
    birth_date = DateField('birth_date')
    choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = SelectField('gender', choices=choices)
