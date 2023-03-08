from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = 'def2618d56f97817dc2eb139b2d63f0c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)
db= SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
loginmanager= LoginManager(app)
loginmanager.login_view = 'login'
loginmanager.login_message_category='info'
from flaskblog import routes