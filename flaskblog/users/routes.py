
from flask import (Blueprint, Markup, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from flaskblog import bcrypt, db
from .forms import (LoginForm, RegisterForm, ResetPasswordForm,
                             ResetPasswordRequestForm, UpdateForm)
from flaskblog.models import User
from flaskblog.users.utils import save_picture,get_reset_token, send_reset_email,verify_token

users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect('home')
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    password=password_hash, email=form.email.data)
        db.session.add(user)
        db.session.commit()

        flash(f"Your account has been created and ready to login", "success")
        return redirect(url_for('users.login'))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('home')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f"Log In Unsuccessfull, check your Email and Password", "danger")

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.img_file = save_picture(form.picture.data)

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated !', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pic/' + current_user.img_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/reset_request",  methods=["GET", "POST"])
def reset_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = get_reset_token(user)
        send_reset_email(user, token)
        msg = f"We've sent an email to <b>{user.email}</b> with instructions to reset your password."
        flash(Markup(msg), 'info')
        return redirect(url_for('main.home'))

    return render_template('reset_request.html', form=form, title='Reset Password Request')


@users.route('/reset_password/<token>', methods=["GET", "POST"])
def password_reset(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        responce_ = verify_token(token)
        if responce_['status'] == 'success':
            user = responce_['value']
            password_hash = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user.password = password_hash
            db.session.add(user)
            db.session.commit()
            flash("Your password has been changed successfully!", "success")
            return redirect(url_for('users.login'))
        else:
            flash(responce_['value'], "success")
            return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form, title='Reset Password')
