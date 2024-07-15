from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///desserts.db'
db = SQLAlchemy(app)


if __name__ == "__main__":


    from user_views import *

    app.run(debug=True)