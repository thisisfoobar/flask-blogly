"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users table"""

    __tablename__ = "users"

    default_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/1200px-Default_pfp.svg.png'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=True,
                          default=default_url)
    
    posts = db.relationship("Post", backref="user",cascade="all, delete-orphan")
        
    @property
    def full_name(self):
        """Return full name of user"""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Show info about user"""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}"
    
class Post(db.Model):
    """Blog post table"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now())
    modified_on = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.datetime.now(),
                            onupdate=datetime.datetime.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)
          
class Tag(db.Model):
    """Tags for posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False)
    
    posts = db.relationship('Post',secondary="post_tags",cascade="all, delete",backref='tags')
    
class PostTag(db.Model):
    """M2M Relationship between Tags and Posts"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)
    
