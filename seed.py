from models import db, User, Post
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