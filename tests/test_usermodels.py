import unittest
from api.__init__ import app, environment_name, databases
from api.v1.UserModel import *

# parses json to string or files (or python dict and []
import json

class ModelTestCases(unittest.TestCase):
    def setUp(self):
        environment_name('TestingEnvironment')
        databases.create_all()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests create user
    def test_create_user(self):
        """Test create user."""
        User.createUser(
            _username="user2",
            _password="password2")

        created_user = User.getAllUsers()[0]

        self.assertEqual(created_user.username, "user2")
        self.assertEqual(created_user.password, "password2")

    # tests getting user
    def test_get_users(self):
        """Test retrieval of user from DB."""
        User.createUser(
            _username="user1",
            _password="password1")

        User.createUser(
            _username="user2",
            _password="password2")
        User.createUser(
            _username="user3",
            _password="password3")

        user_count = len(User.getAllUsers())
        self.assertEqual(3, user_count)

    def test_username_password_match(self):
        User.createUser(_username="user1",
                        _password="password1")
        found = User.username_password_match('user1', 'password1')
        self.assertEqual(found, True)
