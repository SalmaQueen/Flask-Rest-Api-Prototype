
from tests.base_test_case import AuthTestCase


class BookTestCases(AuthTestCase):

    payload = {"name": "bookname", "price": 7.99, "isbn": "9780394800165"}

    # tests that a new book is successfully created
    def test_create_new_book(self):
        self.login()
        response = self.client.post('/api/v1/books', json=self.payload, headers=self.headers)
        self.assertEqual(201, response.status_code)

    # tests creation of book fails without name
    def test_create_new_book_without_name(self):
        self.login()
        payload = {"price": 7.99, "isbn": "9780394800165"}
        response = self.client.post('/api/v1/books', json=payload, headers=self.headers)
        self.assertEqual(400, response.status_code)

    # tests getting a book by isbn
    def test_get_book_by_id(self):
        self.login()
        self.client.post('/api/v1/books', json=self.payload, headers=self.headers)
        response = self.client.get('/api/v1/books/9780394800165')
        self.assertEqual(200, response.status_code)

    # tests updating a book succeeds
    def test_update_book(self):
        self.login()
        self.client.post('/api/v1/books', json=self.payload, headers=self.headers)
        payload = {"name": "booknamena", "price": 9.99, "isbn": 12345678910}
        response = self.client.put('/api/v1/books/9780394800165', json=payload, headers=self.headers)
        self.assertEqual(204, response.status_code)

    # tests deleting a book
    def test_delete_book(self):
        self.login()
        self.client.post('/api/v1/books', json=self.payload, headers=self.headers)
        response = self.client.delete('/api/v1/books/9780394800165', headers=self.headers)
        self.assertEqual(204, response.status_code)

    # tests deleting a non existent book fails
    def test_delete_non_existence_book(self):
        self.login()
        response = self.client.delete('/api/v1/books/1234394800165', json=self.payload, headers=self.headers)
        self.assertTrue(response.status_code, 404)
