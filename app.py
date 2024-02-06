"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, get_flashed_messages
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def user_redirect():
    """redirect to list of users"""
    return redirect("/users")

@app.route("/users")
def users_list():
    """display list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("userlist.html", users=users)

@app.route("/users/new")
def new_user_form():
    """add new user"""
    return render_template("adduser.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """add user to db"""

    first_name = request.form['firstname']
    last_name = request.form['lastname']
    image_url = request.form['url']

    image_url = image_url if image_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    flash(f'User {user.first_name} {user.last_name} Created')

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """display user details"""

    user = User.query.get_or_404(user_id)
    return render_template("userdetails.html",user=user,posts=user.posts)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """display user edit form"""
    user = User.query.get_or_404(user_id)
    return render_template("edituser.html",user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_update(user_id):
    """push changes to user to db"""

    first_name = request.form['firstname']
    last_name = request.form['lastname']
    image_url = request.form['url']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    
    user.image_url = image_url if image_url else user.default_url

    db.session.commit() 

    flash(f'User {user.first_name} {user.last_name} Updated')

    return redirect("/users")

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """delete user from db"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    flash(f'User {user.first_name} {user.last_name} Deleted')

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Add a new post from a user"""
    user = User.query.get_or_404(user_id)

    return render_template("newpost.html",user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add post infomation to db"""

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title,content=content,user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    flash(f"{new_post.title} created")

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def display_post(post_id):
    """Show single post"""

    post = Post.query.get_or_404(post_id)

    return render_template("postdetails.html",post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Edit post"""

    post = Post.query.get_or_404(post_id)

    return render_template("editpost.html",post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_update(post_id):
    """Push updates to db"""

    title = request.form['title']
    content = request.form['content']

    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    flash(f"Post updated successfully")

    return redirect(f"/users/{post.user.id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete posts"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()

    flash(f'Post deleted')

    return redirect(f"/users/{user_id}")