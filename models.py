from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    first_last_name = db.Column(db.String(30))
    second_last_name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(80))
    birth_date = db.Column(db.DateTime)
    gender = db.Column(db.String(1))
    password = db.Column(db.String(64))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(20), nullable=True)
