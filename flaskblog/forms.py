from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField , PasswordField , SubmitField, BooleanField , TextAreaField
from flask_wtf.file import FileField , FileAllowed
from wtforms.validators import Email , DataRequired,EqualTo,Length ,ValidationError
from .models import User,Post

class RegisterForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[ DataRequired() ,EqualTo("password")])
    submit = SubmitField("Sign up")

    def validate_username(self,username =username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username is taken please choose a diffrent one')

    def validate_email(self,email =email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Email is taken please choose a diffrent one')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class UpdateForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField("Email", validators=[DataRequired(),Email()])
    picture= FileField("Update Profile Picture", validators=[FileAllowed(['png','jpeg','jpg'])])
    submit = SubmitField("Update")

    def validate_username(self,username =username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That Username is taken please choose a diffrent one')
    def validate_email(self,email =email):
        if current_user.email != email.data :
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That Email is taken please choose a diffrent one')

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content",validators=[DataRequired()])
    submit = SubmitField("Post")

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self,email =email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('This Email is not registered yet. Please register')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[ DataRequired() ,EqualTo("password")])
    submit = SubmitField("Reset")