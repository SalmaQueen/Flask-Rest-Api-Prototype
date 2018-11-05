import unittest
from api.__init__ import app, environment_name, databases

# parses json to string or files (or python dict and []
import json


class BookTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        environment_name('TestingEnvironment')
        self.payload = json.dumps({"name": "bookname", "price": 7.99, "isbn": "9780394800165"})
        databases.create_all()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests that a new book is successfully created
    def test_create_new_book(self):
        response = self.app.post('/books', data=self.payload)
        self.assertTrue(response.status_code == 201)

    # tests creation of book fails without name
    def test_create_new_book_without_name(self):
        payload = json.dumps({"price": 7.99, "isbn": "9780394800165"})
        response = self.app.post('/books', data=payload)
        self.assertEqual(response.status_code, 400)

    # tests getting a book by isbn
    def test_get_book_by_id(self):
        response = self.app.post('/books', data=self.payload)
        response = self.app.get('/books/9780394800165')
        self.assertEqual(response.status_code, 200)

    # tests updating a book succeeds
    def test_update_book(self):
        response = self.app.post('/books', data=self.payload)
        payload = json.dumps({"name": "booknamena", "price": 9.99, "isbn": 12345678910})
        response = self.app.put('/books/9780394800165', data=payload)
        self.assertEqual(response.status_code, 204)

    # tests deleting a book
    def test_delete_book(self):
        response = self.app.post('/books', data=self.payload)
        response = self.app.delete('/books/9780394800165')
        self.assertEqual(response.status_code, 204)

    # tests deleting a non existent book fails
    def test_delete_non_existence_book(self):
        response = self.app.delete('/books/1234394800165', data=self.payload)
        self.assertTrue(response.status_code, 404)
