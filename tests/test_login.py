import unittest
from api.__init__ import app, environment_name, databases

# parses json to string or files (or python dict and []
import json

'''
 201  ok resulting to  creation of something
 200  ok
 400  bad request
 404  not found
 401  unauthorized
 409  conflict
'''

# tests all functionality of login and possible edge cases
class LoginTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        environment_name('TestingEnvironment')
        databases.create_all()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests login with blank password
    def test_login_blank_password(self):
        payload = json.dumps({"username": "user1", "password": ""})
        response = self.app.post('/login', data=payload)
        self.assertIn('Password is required', response.data.decode('utf-8'))
        self.assertAlmostEqual(response.status_code, 401)

    # tests login with blank username
    def test_login_blank_username(self):
        payload = json.dumps({"username": "", "password": "password"})
        response = self.app.post('/login', data=payload)
        self.assertIn('Username is required', response.data.decode('utf-8'))
        self.assertAlmostEqual(response.status_code, 401)

    # tests login with special characters
    def test_login_with_special_characters_username(self):
        payload = json.dumps({"username": "%$^&user1(", "password": "password"})
        response = self.app.post('/login', data=payload)
        self.assertIn('Username cannot contain special characters', response.data.decode('utf-8'))
        self.assertAlmostEqual(response.status_code, 400)

    '''
    
    # tests login with short password
    def test_login_with_short_password(self):
        payload = json.dumps({"username": "user1", "password": "password"})
        response = self.app.post('/register', data=payload)
        payload = json.dumps({"username": "user1", "password": "pass"})
        response = self.app.post('/login', data=payload)
        self.assertIn('The password is too short', response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)

    # tests login with invalid username
    def test_login__with_invalid_username(self):
        payload = json.dumps({"username": "user1", "password": "password"})
        self.app.post('/register', data=payload)
        payload = json.dumps({"username": "user111", "password": "password"})
        response = self.app.post('/login', data=payload)
        self.assertIn('The Username is invalid', response.data.decode('utf-8'))
        self.assertAlmostEqual(response.status_code, 401)

    # tests login with wrong password
    def test_login_with_wrong_password(self):
        payload = json.dumps({"username": "user1", "password": "password"})
        self.app.post('register', data=payload)
        payload = json.dumps({"username": "user1", "password": "password111"})
        response = self.app.post('/login', data=payload)
        self.assertIn('The is incorrect', response.data.decode('utf-8'))
        self.assertAlmostEqual(response.status_code, 401)

'''

       