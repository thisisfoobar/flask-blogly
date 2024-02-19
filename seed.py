from models import db, User, Post, Tag, PostTag
from app import app

# Drop and recreate tables
db.drop_all()
db.create_all()

# Create several users
u1 = User(first_name='Gene', last_name='Evergreen')
u2 = User(first_name='Augie', last_name='Evergreen')
u3 = User(first_name='Otter',last_name='King')
u4 = User(first_name='Morla',last_name='King')

db.session.add_all([u1,u2,u3,u4])
db.session.commit()

p1 = Post(title="A Day in Gene's Life", content="My life", user_id=1)
p2 = Post(title="A Day in Augie's Life", content="My life", user_id=2)
p3 = Post(title="A Day in Otter's Life", content="My life", user_id=3)
p4 = Post(title="A Day in Morla's Life", content="My life", user_id=4)

db.session.add_all([p1,p2,p3,p4])
db.session.commit()

t1 = Tag(name="Litter Box")
t2 = Tag(name="Food")
t3 = Tag(name="Treats")
t4 = Tag(name="Squirrel")

db.session.add_all([t1,t2,t3,t4])
db.session.commit()

pt1 = PostTag(post_id=1,tag_id=1)
pt2 = PostTag(post_id=2,tag_id=1)
pt3 = PostTag(post_id=3,tag_id=1)
pt4 = PostTag(post_id=1,tag_id=2)

db.session.add_all([pt1,pt2,pt3,pt4])
db.session.commit()