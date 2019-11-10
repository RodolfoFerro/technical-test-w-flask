from datetime import datetime

from flask import render_template
from flask import request
from flask import jsonify
from flask import session
from flask import url_for
from flask import redirect

from app import db
from app import app
from models import User
from forms import LoginForm
from utils import parse_users
from hash import hash_password
from hash import verify_password_hash


# ===============================================================
# ======================== BASE URL =============================
# ===============================================================
@app.route('/', methods=['GET'])
def index():
    """Base url to test app."""

    # Pop previous session:
    session.pop('user', None)
    session.pop('email', None)

    return render_template('index.html')


# ===============================================================
# ======================= LOGIN VIEW ============================
# ===============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login url."""

    # Pop previous session:
    session.pop('user', None)
    session.pop('email', None)

    # Login flag and form:
    login_error = False
    form = LoginForm(request.form)

    if len(form.errors):
        print(form.errors)
    if request.method == 'POST':
        # Fetch data from login form:
        email = form.email.data
        password = form.password.data

        # Fetch query from databse:
        query = User.query.filter_by(email=email).first()

        # Validate query and extract attributes:
        if query:
            hash_pass = getattr(query, 'password')
            name = getattr(query, 'name')
            fst_ln = getattr(query, 'first_last_name')
            snd_ln = getattr(query, 'second_last_name')

            # Validate password and create session:
            if verify_password_hash(password, hash_pass):
                session['email'] = email
                session['user'] = f'{name} {fst_ln} {snd_ln}' if snd_ln \
                                    else f'{name} {fst_ln}'

                return render_template('success_login.html', session=session)
            else:
                login_error = True

    return render_template('login.html', login_error=login_error)


# ===============================================================
# ====================== CRUD SECTION ===========================
# ===============================================================
@app.route('/create', methods=['POST'])
def create():
    """CREATE url to add users."""

    # Fetch JSON from POST request:
    data = request.get_json()

    # Validate birth date:
    try:
        date = data['birth_date'].split('/')
        date = [int(item) for item in date[::-1]]
    except Exception as e:
        print('[ERROR] ' + e)
        response = {
            'response': '[ERROR] Birth date must be in "DD/MM/YYYY" format.'
        }
        return jsonify(response)

    # Validate gender:
    if data['gender'] not in ['M', 'F', 'O']:
        response = {
            'response': '[ERROR] Gender must be in "M", "F" or "O".'
        }
        return jsonify(response)

    # Validate second last name:
    sln = data['second_last_name'] if 'second_last_name' in data else None

    # Create user to append into database:
    user = User(
                name = data['name'],
                first_last_name = data['first_last_name'],
                second_last_name = sln,
                email = data['email'],
                birth_date = datetime(date[0], date[1], date[2]),
                gender = data['gender'],
                password = hash_password(data['password'])
            )

    # Add generated user to database:
    db.session.add(user)
    db.session.commit()

    # Generate and return response:
    response = {
        'response': '[INFO] User successfully added to database.'
    }

    return jsonify(response)


@app.route('/read/<int:id>', methods=['GET'])
def read(id):
    """READ url to fetch users."""

    # Fetch user from database:
    query = User.query.filter_by(id=id).first()

    # Build response:
    response = {
        'response': '[INFO] User info correctly gathered from database.',
        'user': {
            key: ( getattr(query, key) if key != 'birth_date' \
                    else getattr(query, key).strftime("%d/%m/%Y") ) \
                for key in query.__table__.columns._data.keys()
        }
    } if query else {
        'response': f'[ERROR] User with id {id} not found in database.'
    }

    return jsonify(response)


@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    """PUT url to update users."""

    # Fetch JSON from PUT request:
    data = request.get_json()

    # Fetch user from database:
    query = User.query.filter_by(id=id).first()

    # Validate non-empty query and update data:
    if query:
        for key, value in data.items():
            if key == 'birth_date':
                # Validate birth date:
                try:
                    date = value.split('/')
                    date = [int(item) for item in date[::-1]]
                    setattr(query, key, datetime(date[0], date[1], date[2]))
                except Exception as e:
                    print('[ERROR] ' + e)
                    response = {
                        'response':
                        '[ERROR] Birth date must be in "DD/MM/YYYY" format.'
                    }
                    return jsonify(response)
            else:
                setattr(query, key, value)
        db.session.commit()

    # Build response:
    response = {
        'response': '[INFO] User info correctly updated into database.',
        'user': {
            key: ( getattr(query, key) if key != 'birth_date' \
                    else getattr(query, key).strftime("%d/%m/%Y") ) \
                for key in query.__table__.columns._data.keys()
        }
    } if query else {
        'response': f'[ERROR] User with id {id} not found in database.'
    }


    return jsonify(response)


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    """DELETE url to remove users."""

    # Fetch user from database:
    query = User.query.filter_by(id=id).first()

    # Build response:
    response = {
        'response': '[INFO] User info correctly removed from database.',
        'user': {
            key: ( getattr(query, key) if key != 'birth_date' \
                    else getattr(query, key).strftime("%d/%m/%Y") ) \
                for key in query.__table__.columns._data.keys()
        }
    } if query else {
        'response': f'[ERROR] User with id {id} not found in database.'
    }

    if query:
        db.session.delete(query)
        db.session.commit()

    return jsonify(response)


# ===============================================================
# ======================== USERS URL ============================
# ===============================================================
@app.route('/users', methods=['GET', 'POST'])
def users():
    """Users url to display table with registered users."""

    if request.method == 'POST' and request.form['del']:
        id = request.form['del']

        # Fetch user from database:
        query = User.query.filter_by(id=id).first()
        db.session.delete(query)
        db.session.commit()

    # Fetch all users from database:
    query = User.query.all()
    users = parse_users(query)

    return render_template('users.html', users=users)


@app.route('/user/<int:id>', methods=['GET'])
def user_id(id):
    """User url to display detailed info from user."""

    # Fetch user from database:
    query = User.query.filter_by(id=id).first()

    if query:
        user = {
            key: ( getattr(query, key) if key != 'birth_date' \
                    else getattr(query, key).strftime("%d/%m/%Y") ) \
                for key in query.__table__.columns._data.keys()
        }

        if not user['second_last_name']:
            user['username'] = user['name'] + \
                                user['first_last_name']
        else:
            user['username'] = user['name'] + \
                                user['first_last_name'] + \
                                user['second_last_name']
        return render_template("user.html", user=user)
    else:
        return redirect(url_for('error_404', user=id))


# ===============================================================
# ====================== ERROR HANDLER ==========================
# ===============================================================
@app.route('/not-found')
@app.errorhandler(404)
def error_404(error=None):
    user = request.args.get('user') or None
    return render_template('404.html', user=user)
