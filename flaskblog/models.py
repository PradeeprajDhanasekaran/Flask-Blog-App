from flaskblog import db ,loginmanager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer


@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key= True)
    username = db.Column(db.String(24),unique=True,nullable =False)
    email = db.Column(db.String(120), unique= True, nullable =False)
    password = db.Column(db.String(20), nullable =False)
    img_file = db.Column(db.String(20),nullable =False , default = 'default.jpeg')
    posts = db.relationship("Post",backref = 'author',lazy = True)
    def __repr__(self):
        return f'User {self.username},{self.email},{self.img_file}'

class Post(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text() , nullable = False)
    date_posted = db.Column(db.DateTime,nullable = False,default = datetime.utcnow )
    user_id = db.Column(db.Integer ,db.ForeignKey('user.id'), nullable = False)
    def __repr__(self):
        return f'Post {self.title},{self.date_posted}'
