from datetime import datetime
from flask import Flask,render_template , url_for ,flash, redirect
from forms import RegisterForm, LoginForm 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'def2618d56f97817dc2eb139b2d63f0c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db= SQLAlchemy(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
class User(db.Model):
    id = db.Column(db.Integer(),primary_key= True)
    username = db.Column(db.String(24),unique=True,nullable =False)
    email = db.Column(db.String(120), unique= True, nullable =False)
    password = db.Column(db.String(20), nullable =False)
    img_file = db.Column(db.String(20),nullable =False , default = 'default.jpg')
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

posts = [{
    "author":"Pradeep Raj",
    "title": "Blog Post 1",
    "content" : "1st post content",
    "date_created" : "Nov 2, 2019"
                               
},{
    "author":"Ibrahim",
    "title": "Blog Post 2",
    "content" : "2nd post content",
    "date_created" : "Nov 2, 2020"
                               
},{
    "author":"Mari",
    "title": "Blog Post 3",
    "content" : "3rd post content",
    "date_created" : "Sep 9, 2021"
                               
}]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts)
    
@app.route("/about")
def about():
    return render_template("about.html" , title ="About Page")

@app.route("/register", methods =["GET","POST"] )
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"Account has been created for {form.username.data}","success")
        return redirect(url_for('home'))

    return render_template("register.html" , title ="Register",form= form)

@app.route("/login", methods =["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@gmail.com' and form.password.data == "test":
            flash(f"You have been logged in successfully ","success")
            return redirect(url_for('home'))
        else:
            flash(f"Log In Unsuccessfull, check your Email and Password","danger")

        
    return render_template("login.html" , title ="Login",form= form)

if __name__ == '__main__':

    app.run(debug=True)

    