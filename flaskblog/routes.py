from flaskblog.models import User,Post
from flask import render_template , url_for ,flash, redirect
from flaskblog.forms import RegisterForm, LoginForm 
from flaskblog import app, bcrypt ,db
from flask_login import login_user ,logout_user ,current_user

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
    if current_user.is_authenticated :
        return redirect('home')
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data ,password= password_hash ,email =form.email.data)
        db.session.add(user)
        db.session.commit()

        flash(f"Your account has been created and ready to login","success")
        return redirect(url_for('login'))

    return render_template("register.html" , title ="Register",form= form)

@app.route("/login", methods =["GET","POST"])
def login():
    if current_user.is_authenticated :
        return redirect('home')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) :
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f"Log In Unsuccessfull, check your Email and Password","danger")

        
    return render_template("login.html" , title ="Login",form= form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))