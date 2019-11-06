import uuid
import os


SECRET_KEY = uuid.uuid4().hex
DEBUG = True

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'challenge.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
