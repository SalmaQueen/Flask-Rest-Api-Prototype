import json
import unittest
from unittest.mock import patch
import jwt
from datetime import datetime

from run import app


class TestDecorators(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client(use_cookies=False)

    @patch.object(jwt, 'decode')
    def test_token_required(self, patched_decode):
        expiration_date = datetime.utcnow()
        token = jwt.encode({'exp': expiration_date}, self.app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

        resp = self.client.get('/something?token={}'.format(token))

        patched_decode.assert_called_with(token, self.app.config['SECRET_KEY'])

        self.assertEqual(resp.status_code, 200)

    def test_token_required_incorrect(self):
        # Just test that if you give it no token, it breaks
        resp = self.client.get('/something')
        self.assertIn('error', json.loads(resp.get_data()))