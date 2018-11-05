import unittest
from unittest.mock import patch
from run import app
from api.v1.BookModel import Book
import json
from api.v1.UserModel import User
import datetime
import jwt


class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client(use_cookies=False)

    @patch.object(jwt, 'encode')
    @patch.object(datetime, 'datetime')
    @patch.object(User, 'username_password_match')
    def test_get_token(self, mock_match_method, mock_datetime, jwt_encode_mock):
        mock_match_method.return_value = True

        now = datetime.datetime.utcnow()

        mock_datetime.utcnow.return_value = now

        token = 'fake_token'
        jwt_encode_mock.return_value = token

        username = 'someuser'
        password = 'somepassword'
        response = self.client.post(
            '/login',
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json'
        )

        self.assertEquals(response.get_data().decode('utf-8'), token)

        jwt_encode_mock.assert_called_with(
            {'exp': now + datetime.timedelta(seconds=100)},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        jwt_encode_mock.assert_called_once()

        mock_match_method.assert_called_with(username, password)

    @patch.object(Book, 'add_book')
    def test_post_books(self, patched_add_book):
        name = 'somename'
        isbn = 'someisbn'
        price = 50
        data = {
            'name': name,
            'isbn': isbn,
            'price': price
        }

        resp = self.client.post('/books', data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        # Assert that add book was called with the right arguments
        patched_add_book.assert_called_with(name, price, isbn)