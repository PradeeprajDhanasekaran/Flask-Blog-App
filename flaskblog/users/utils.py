from flask import url_for ,current_app
from flaskblog.models import User
from flaskblog import mail
from secrets import token_hex
import datetime
from flask_mail import Message
import jwt
from jwt.exceptions import InvalidTokenError
from PIL import Image
import os


def save_picture(picture):
    random_hex = token_hex(8)
    _ , ext_ = os.path.splitext(picture.filename)
    file_name = random_hex + ext_
    full_path = os.path.join(current_app.root_path , 'static/profile_pic' , file_name)
    size =(125,125)
    img = Image.open(picture)
    img.thumbnail(size)
    img.save(full_path)
    return file_name

def get_reset_token(user):
    payload= {"user_id":user.id ,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}
    token = jwt.encode(payload, current_app.config['SECRET_KEY'],algorithm='HS256')
    return token
    
def verify_token(token):
    try:
        payload = jwt.decode(token,current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id =payload['user_id']
    except InvalidTokenError :
        return {'value': 'Your password reset link has expired. Please request a new link to reset your password.','status':'error'}
    return {'value': User.query.get(user_id), 'status':'success'}
    


def send_reset_email(user,token):
    msg = Message(
        'Password Reset', recipients=[user.email]
    )
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.password_reset',token=token,_external=True)}'''
    mail.send(msg)
