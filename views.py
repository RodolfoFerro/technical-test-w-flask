from datetime import datetime

from flask import render_template
from flask import redirect
from flask import request
from flask import jsonify
from flask import session
from flask import url_for
from sqlalchemy import or_

from app import db
from app import app
from models import User
from forms import UserForm
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
    login_flag = False
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
                login_flag = True
                session['email'] = email
                session['user'] = f'{name} {fst_ln} {snd_ln}' if snd_ln \
                                    else f'{name} {fst_ln}'

                return render_template(
                            'success_login.html',
                            session=session,
                            login_flag=login_flag
                        )
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
                name=data['name'],
                first_last_name=data['first_last_name'],
                second_last_name=sln,
                email=data['email'],
                birth_date=datetime(date[0], date[1], date[2]),
                gender=data['gender'],
                password=hash_password(data['password'])
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
# ================== USERS + ?filter={name} =====================
# ====================== EDIT USER URL ==========================
# ===============================================================
@app.route('/users', methods=['GET', 'POST'])
def users():
    """Users url to display table with registered users."""

    editable = False

    if request.method == 'POST':
        if request.form['del']:
            id = request.form['del']

            # Fetch user from database:
            query = User.query.filter_by(id=id).first()
            db.session.delete(query)
            db.session.commit()

    if request.method == 'GET' and request.args:
        # Filter name by GET method:
        f = request.args['filter']
        filter = or_(
                    User.name.contains(f),
                    User.first_last_name.contains(f),
                    User.second_last_name.contains(f)
                )
        query = User.query.filter(filter).all()
        users = parse_users(query)

        return render_template('users.html', users=users)

    # Validate if the user has successfully logged in:
    if 'user' in session:
        editable = True

    # Fetch all users from database:
    query = User.query.all()
    users = parse_users(query)

    return render_template('users.html', users=users, editable=editable)


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


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    """User url for edition."""

    # Validate session:
    if not 'user' in session:
        return redirect('/error_404')
    else:
        # Fetch user from database:
        query = User.query.filter_by(id=id).first()

        if query:
            form = UserForm(request.form)

            if len(form.errors):
                print(form.errors)
            if request.method == 'POST':
                # Fetch data from user edit form:
                user_data = {
                    'name': form.name.data,
                    'first_last_name': form.first_last_name.data,
                    'second_last_name': form.second_last_name.data,
                    'email': form.email.data,
                    'password': form.password.data,
                    'birth_date': form.birth_date.data,
                    'gender': form.gender.data
                }

                for key, value in user_data.items():
                    setattr(query, key, value)

                # Commit update to database:
                db.session.commit()

                return redirect(url_for('users'))

            user = {
                key: ( getattr(query, key) if key != 'birth_date' \
                        else getattr(query, key).strftime("%d/%m/%Y") ) \
                    for key in query.__table__.columns._data.keys()
            }

            if not user['second_last_name']:
                user['username'] = user['name'] + ' ' + \
                                    user['first_last_name']
            else:
                user['username'] = user['name'] + ' ' + \
                                    user['first_last_name'] + ' ' + \
                                    user['second_last_name']
            return render_template("user-edit.html", user=user, form=form)
        else:
            return redirect(url_for('error_404', user=id))


@app.route('/new', methods=['GET', 'POST'])
def new_user():
    """User url for creation."""

    form = UserForm(request.form)

    # Validate session:
    if not 'user' in session:
        return redirect('/error_404')
    else:
        if request.method == 'POST':
            if len(form.errors):
                print(form.errors)
            if request.method == 'POST':
                # Validate second last name:
                if len(form.second_last_name.data):
                    sln = form.second_last_name.data
                else:
                    sln = None

                # Fetch data from user edit form:
                data = {
                    'name': form.name.data,
                    'first_last_name': form.first_last_name.data,
                    'second_last_name': sln,
                    'email': form.email.data,
                    'password': form.password.data,
                    'birth_date': form.birth_date.data,
                    'gender': form.gender.data
                }


                # Create user to append into database:
                user = User(
                            name=data['name'],
                            first_last_name=data['first_last_name'],
                            second_last_name=sln,
                            email=data['email'],
                            birth_date=data['birth_date'],
                            gender=data['gender'],
                            password=hash_password(data['password'])
                        )

                # Add generated user to database:
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('users'))

        return render_template("user-edit.html", user=None, form=form)


# ===============================================================
# ====================== ERROR HANDLER ==========================
# ===============================================================
@app.route('/not-found')
@app.errorhandler(404)
def error_404(error=None):
    user = request.args.get('user') or None
    return render_template('404.html', user=user)
