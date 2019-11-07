from app import db


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(30))
    first_last_name = db.Column('first_last_name', db.String(30))
    second_last_name = db.Column('second_last_name', db.String(30), nullable=True)
    email = db.Column('email', db.String(80))
    birth_date = db.Column('birth_date', db.DateTime)
    gender = db.Column('gender', db.String(1))
    password = db.Column('password', db.String(64))

    def __init__(self, name, first_last_name, second_last_name,
                 email, birth_date, gender, password):
        self.name = name
        self.first_last_name = first_last_name
        self.second_last_name = second_last_name
        self.email = email
        self.birth_date = birth_date
        self.gender = gender
        self.password = password


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(20), nullable=True)
