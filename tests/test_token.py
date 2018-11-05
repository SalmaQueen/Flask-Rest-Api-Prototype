import unittest
from unittest.mock import MagicMock
from api.__init__ import app, environment_name, databases
from api.v1.UserModel import *
import datetime

# parses json to string or files (or python dict and []
import json

import time


class TokenTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        environment_name('TestingEnvironment')
        databases.create_all()

        User.createUser(
            _username="user1",
            _password="password1")

        self.payload = json.dumps({"username": "user1", "password": "password1"})

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_get_token(self):
        self.app.post("/login", data=self.payload, headers={'Content-Type': 'application/json'})
        response = self.app.post("/login", data=self.payload, headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)

    def test_token_expires(self):
        time_delta = datetime.timedelta(milliseconds=0)
        datetime.timedelta = MagicMock()
        datetime.timedelta.return_value = time_delta

        response = self.app.post("/login", data=self.payload, headers={'Content-Type': 'application/json'})
        access_token = response.data.decode('Utf-8')
        token = access_token

        time.sleep(1)

        response = self.app.get("/books?token=" + token)
        self.assertEqual(401, response.status_code)


if __name__ == '__main__':
    unittest.main()
