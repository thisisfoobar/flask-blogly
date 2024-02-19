"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, get_flashed_messages
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)

"""Home page"""
@app.route("/")
def user_redirect():
    """Display Home Page"""

    posts = Post.query.limit(5).all()

    return render_template("home.html",posts=posts)

"""Users routes"""
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
    tags = Tag.query.all()

    return render_template("newpost.html",user=user,tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add post infomation to db"""

    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title,content=content,user_id=user_id,tags=tags)
    db.session.add(new_post)
    db.session.commit()

    flash(f"{new_post.title} created")

    return redirect(f"/users/{user_id}")

"""Post routes"""
@app.route("/posts/<int:post_id>")
def display_post(post_id):
    """Show single post"""

    post = Post.query.get_or_404(post_id)

    return render_template("postdetails.html",post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Edit post"""
    tags = Tag.query.all()
    post = Post.query.get_or_404(post_id)

    return render_template("editpost.html",post=post,tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_update(post_id):
    """Push updates to db"""

    title = request.form['title']
    content = request.form['content']

    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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

"""Tag routes"""
@app.route("/tags")
def tags_list():
    """Display list of all tags"""

    tags = Tag.query.all()

    return render_template("taglist.html", tags=tags)

@app.route("/tags/new")
def add_tag_form():
    """Display form to add new tag"""

    return render_template("newtag.html")

@app.route("/tags/new",methods=["POST"])
def add_tag():
    """Push new tag to database"""
    name = request.form['name']

    all_tags = Tag.query.with_entities(Tag.name).all()
    upper_tags = [tag[0].upper() for tag in all_tags]

    if name.upper() in upper_tags:
        flash(f"{name} already exists")
        return redirect("/tags")
    else:
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()

        flash(f"{new_tag.name} created")

        return redirect("/tags")
    
@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show tag and associated posts"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("tagdetails.html",tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """display form to update tag info"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edittag.html",tag=tag)

@app.route("/tags/<int:tag_id>/edit",methods=["POST"])
def edit_tag_update(tag_id):
    """update tag in the database"""

    tag = Tag.query.get_or_404(tag_id)
    old_name = tag.name
    name = request.form['name']

    all_tags = Tag.query.with_entities(Tag.name).all()
    upper_tags = [tag[0].upper() for tag in all_tags]

    if name.upper() in upper_tags:
        flash(f"{name} already exists, edit not saved")
        return redirect("/tags")
    else:
        tag.name = name
        db.session.add(tag)
        db.session.commit()

        flash(f"{old_name} updated to {tag.name}")

        return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete",methods=["POST"])
def delete_tag(tag_id):
    """delete tag from the database"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f"{tag.name} deleted")

    return redirect("/tags")
