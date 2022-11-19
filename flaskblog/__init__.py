from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = 'def2618d56f97817dc2eb139b2d63f0c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db= SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
loginmanager= LoginManager(app)
from flaskblog import routes