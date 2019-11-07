from datetime import datetime  # datetime.now().strftime("%d/%m/%Y")

from flask import render_template
from flask import request
from flask import jsonify
from flask import session

from app import db
from app import app
from models import User
from forms import LoginForm
from hash import hash_password
from hash import verify_password_hash


# ===============================================================
# ======================== BASE URL =============================
# ===============================================================
@app.route('/', methods=['GET'])
def base_url():
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

    # Validate non-empty query:
    if query:
        keys = query.__table__.columns._data.keys()

    # Build response:
    response = {
        'response': '[INFO] User info correctly gathered from database.',
        'user': {
            key: ( getattr(query, key) if key != 'birth_date' \
                    else getattr(query, key).strftime("%d/%m/%Y") ) \
                for key in keys
        }
    } if query else {
        'response': f'[ERROR] User with id {id} not found in database.'
    }

    return jsonify(response)


@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    """PUT url to update users."""

    return True


@app.route('/delete', methods=['DELETE'])
def delete():
    """DELETE url to add users."""

    return True
