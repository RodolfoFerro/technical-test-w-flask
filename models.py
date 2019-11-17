from app import db


class User(db.Model):
    """User model for database."""

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(30))
    first_last_name = db.Column('first_last_name', db.String(30))
    second_last_name = db.Column('second_last_name', db.String(30), nullable=True)
    email = db.Column('email', db.String(80))
    birth_date = db.Column('birth_date', db.DateTime)
    gender = db.Column('gender', db.String(1))
    password = db.Column('password', db.String(64))

    # One-to-one relationship:
    # role = db.relationship('Role', backref='user', uselist=False)


class Role(db.Model):
    """Role model for database."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(20), nullable=True)

    # One-to-one relationship:
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
