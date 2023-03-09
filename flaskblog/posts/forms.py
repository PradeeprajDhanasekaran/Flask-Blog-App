from wtforms import StringField , PasswordField , SubmitField, BooleanField , TextAreaField
from wtforms.validators import Email , DataRequired,EqualTo,Length ,ValidationError
from flask_wtf import FlaskForm

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content",validators=[DataRequired()])
    submit = SubmitField("Post")
