from app.models import User
from tests.base_test_case import AuthTestCase


class TestUser(AuthTestCase):

    def test_can_set_password(self):
        user = User.query.first()
        user.password = 'abc'

    def test_password_is_hashed(self):
        user = User.query.first()
        user.password = 'abc'
        self.assertNotEqual(user.password_hash, 'abc')

    def test_password_is_not_readable(self):
        user = User.query.first()
        with self.assertRaises(AttributeError):
            _ = user.password

    def test_verify_password(self):
        user = User.query.first()
        user.password = 'abc'
        self.assertTrue(user.verify_password('abc'))


