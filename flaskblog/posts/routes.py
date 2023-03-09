from flask import Blueprint,request,render_template
from flaskblog.models import User,Post
from flask import render_template , url_for ,flash, redirect ,request, abort 
from .forms import PostForm 
from flaskblog import db 
from flask_login import current_user, login_required


posts = Blueprint('posts',__name__)


@posts.route("/post/new", methods =["GET","POST"])
@login_required
def new_post(): 
    
    form = PostForm()
    if form.validate_on_submit():
        posts= Post(title=form.title.data, content=form.content.data, author=current_user )
        db.session.add(posts)
        db.session.commit()
        flash("Your post has been created!","success")
        return redirect(url_for("main.home"))
    return render_template('create_post.html',title='New Post',form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)


@posts.route("/post/<int:post_id>/update", methods =["GET","POST"])
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
        return redirect(url_for('posts.post',post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post',form=form,legend='Update Post')
   

@posts.route("/post/<int:post_id>/delete", methods =["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author :
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('main.home'))

@posts.route("/user/<string:username>")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1, type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
    return render_template("user_post.html", posts = posts, user=user)
