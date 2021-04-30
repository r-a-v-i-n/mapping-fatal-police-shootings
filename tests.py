# sum(votes.upvote_downvote)
# this allows us to see the total upvote vs downvote because 
# if there are more -1 than +1, it will reflect the downvotes (& vice versa)
from unittest import TestCase
from server import app
from model import connect_to_db, db, test_data
from flask import session


class FlaskTests(TestCase):

    def setUp(self):
        """Run code before each test"""
        
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage"""

        result = self.client.get("/")
        self.assertIn(b"Home", result.data)


class FlaskTestsDatabase(TestCase):

    def setUp(self):
        """Run code before each test"""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        test_data()

    def tearDown(self):
        """Run this at the end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_signup(self):
        """Test sign up"""

        result = self.client.post('/sign_up',
                                   data={"username":"bjorno", 
                                        "password":"woofwoof626", 
                                        "email":"haulinauss@gmail.com", 
                                        "city":"Columbus", 
                                        "state":"Ohio"},
                                   follow_redirects=True)
        self.assertIn(b'<h1>Log In to your Account</h1>', result.data)

    def test_login(self):
        """Test login"""

        result = self.client.post('/login',
                                   data={"username":"bjorno", 
                                        "password":"woofwoof626"},
                                   follow_redirects=True)
        self.assertIn(b'<h1>MAPPING FATAL POLICE SHOOTINGS</h1>', result.data)
    
    def test_resources(self):
        """Test the resources page"""

        result = self.client.get('/resources',
                                data={"org_name":"Detroit Will Breathe", 
                                        "url":"https://detroitwillbreathe.info/", 
                                        "email":"detroitwillbreathe@protonmail.com", 
                                        "phone":"(313) 473-9658", 
                                        "city":"Detroit",
                                        "state":"Michigan"},
                                follow_redirects=True)
        self.assertIn(b'<h1>Organizations and Resources to Support</h1>', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()