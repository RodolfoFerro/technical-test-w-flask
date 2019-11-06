from datetime import datetime  # datetime.now().strftime("%d/%m/%Y")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


if __name__ == '__main__':
    from views import *
    app.run(host='0.0.0.0', port=5000, debug=True)
