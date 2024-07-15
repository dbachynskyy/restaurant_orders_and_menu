from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///desserts.db'
db = SQLAlchemy(app)


if __name__ == "__main__":

    app.app_context().push()
    db.create_all()
    
    from views import *

    app.run(debug=True)

