from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for users."""

    def setUp(self):
        PostTag.query.delete()


        """Add test user"""
        test_user = User(first_name="TestUser",last_name="TestLast",image_url="www.google.com")
        db.session.add(test_user)
        db.session.commit()

        self.user_id = test_user.id

        """Add test Post"""
        test_post = Post(title="TestPost",content="TestContent",user_id=1)
        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

        """Add test Tag"""
        test_tag = Tag(name="TestTag")
        db.session.add(test_tag)
        db.session.commit()

        self.tag_id = test_tag.id

        """Add test PostTag relationship"""
        test_posttag = PostTag(post_id=1,tag_id=1)
        db.session.add(test_posttag)
        db.session.commit()

    def tearDown(self):
        """Clean up any issues"""

        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Home', html)
# Test User Routes
    def test_users_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>TestUser TestLast</h2>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {'firstname': 'Test2', 'lastname':'Last2', 'url':'www.image.com'}
            resp = client.post(f'/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test2', html)

# Test Post Routes
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<u>TestPost</u>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {'title': 'Test2', 'content':'Last2'}
            resp = client.post(f'/posts/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test2', html)

# Test Tag Routes
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/tags')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {'name': 'Test2'}
            resp = client.post(f'/tags/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test2', html)
