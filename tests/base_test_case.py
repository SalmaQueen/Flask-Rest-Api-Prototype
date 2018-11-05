import unittest

from app import create_app
from app.models import User
from app.extensions import db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class AuthTestCase(BaseTestCase):

    username = 'test'
    password = 'password'

    payload = dict(username=username, password=password)

    def setUp(self):
        super(AuthTestCase, self).setUp()
        user = User(username=self.username)
        user.password = self.password
        db.session.add(user)
        db.session.commit()
        self.headers = dict()

    def login(self):
        resp = self.client.post(self.app.config['JWT_AUTH_URL_RULE'], json=dict(
            username=self.username,
            password=self.password
        ))

        self.headers = {
            'Authorization': 'JWT {}'.format(resp.get_json().get('access_token'))
        }

        return resp



