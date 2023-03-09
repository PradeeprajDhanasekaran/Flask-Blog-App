from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config



mail = Mail()
db= SQLAlchemy()
bcrypt = Bcrypt()
loginmanager= LoginManager()
loginmanager.login_view = 'users.login'
loginmanager.login_message_category='info'



def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    loginmanager.init_app(app)  

    return app