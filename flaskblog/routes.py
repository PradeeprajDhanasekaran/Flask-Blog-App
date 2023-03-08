from flaskblog.models import User,Post
from flask import render_template , url_for ,flash, redirect ,request, abort , Markup
from flaskblog.forms import RegisterForm, LoginForm ,UpdateForm,PostForm , ResetPasswordRequestForm,ResetPasswordForm
from flaskblog import app, bcrypt ,db ,mail
from flask_login import login_user ,logout_user ,current_user, login_required
from secrets import token_hex
import datetime
from flask_mail import Message
import jwt
from jwt.exceptions import InvalidTokenError
from PIL import Image
import os



@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page',1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"Log In Unsuccessfull, check your Email and Password","danger")

        
    return render_template("login.html" , title ="Login",form= form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(picture):
    random_hex = token_hex(8)
    _ , ext_ = os.path.splitext(picture.filename)
    file_name = random_hex + ext_
    full_path = os.path.join(app.root_path , 'static/profile_pic' , file_name)
    size =(125,125)
    img = Image.open(picture)
    img.thumbnail(size)
    img.save(full_path)
    return file_name
   

@app.route("/account", methods =["GET","POST"])
@login_required
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        if form.picture.data :
            current_user.img_file = save_picture(form.picture.data)

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated !','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data= current_user.username
        form.email.data= current_user.email
    image_file = url_for('static', filename='profile_pic/'+ current_user.img_file)
    return render_template('account.html',title='Account',image_file=image_file ,form=form)


@app.route("/post/new", methods =["GET","POST"])
@login_required
def new_post(): 
    
    form = PostForm()
    if form.validate_on_submit():
        posts= Post(title=form.title.data, content=form.content.data, author=current_user )
        db.session.add(posts)
        db.session.commit()
        flash("Your post has been created!","success")
        return redirect(url_for("home"))
    return render_template('create_post.html',title='New Post',form=form, legend='New Post')

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)


@app.route("/post/<int:post_id>/update", methods =["GET","POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author :
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post',form=form,legend='Update Post')
   

@app.route("/post/<int:post_id>/delete", methods =["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author :
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1, type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
    return render_template("user_post.html", posts = posts, user=user)



def get_reset_token(user):
    payload= {"user_id":user.id ,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}
    token = jwt.encode(payload, app.config['SECRET_KEY'],algorithm='HS256')
    return token
    
def verify_token(token):
    try:
        payload = jwt.decode(token,app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id =payload['user_id']
    except InvalidTokenError :
        return {'value': 'Your password reset link has expired. Please request a new link to reset your password.','status':'error'}
    return {'value': User.query.get(user_id), 'status':'success'}
    


def send_reset_email(user,token):
    msg = Message(
        'Password Reset', recipients=[user.email]
    )
    msg.body = f'''To reset your password, visit the following link:
    {url_for('password_reset',token=token,_external=True)}'''
    mail.send(msg)




@app.route("/reset_request",  methods =["GET","POST"])
def reset_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token=get_reset_token(user)
        send_reset_email(user,token)
        msg=f'We’ve sent an email to <b>{user.email}</b> with instructions to reset your password.'
        flash(Markup(msg), 'info')
        return redirect(url_for('home'))

    return render_template('reset_request.html',form=form, title= 'Reset Password Request')

@app.route('/reset_password/<token>', methods =["GET","POST"])
def password_reset(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        responce_=verify_token(token)
        if responce_['status'] == 'success':
            user = responce_['value'] 
            password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = password_hash
            db.session.add(user)
            db.session.commit()
            flash("Your password has been changed successfully!","success")
            return redirect(url_for('login'))
        else:
            flash(responce_['value'],"success")
            return redirect(url_for('login'))
    return render_template('reset_password.html',form=form, title ='Reset Password')
