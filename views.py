from flask import render_template
from flask import request

from app import app
from forms import LoginForm


@app.route('/', methods=['GET'])
def base_url():
    """Base url to test app."""

    response = '<h1>Hello world!</h1>'

    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login url."""

    login_error = False
    form = LoginForm(request.form)

    if len(form.errors):
        print(form.errors)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        print(username, password)
        if username != 'admin' and password != 'admin':
            login_error = True

    return render_template('login.html', login_error=login_error)
