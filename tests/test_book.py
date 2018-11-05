import unittest
from unittest.mock import patch, Mock
from api.v1.BookModel import Book
from api.__init__ import databases, environment_name


class TestBook(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        environment_name('TestingEnvironment')
        cls.mock_books = [
            {
                'name': 'somebook',
                'price': 50,
                'isbn': 'someisbn'
            },
            {
                'name': 'someotherbook',
                'price': 40,
                'isbn': 'myisbn'
            }
        ]

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    @patch.object(databases, 'session')
    def test_add_book(self, patched_session):
        mock_book = self.mock_books[0]
        Book.add_book(_name=mock_book['name'], _isbn=mock_book['isbn'], _price=mock_book['price'])

        patched_session.add.assert_called_once()
        patched_session.commit.assert_called_once()

    @patch.object(Book, 'json')
    @patch.object(Book, 'query')
    def test_get_all_books(self, patched_book_query, patched_book_json):
        mock_book_objects = [Book(**book_data) for book_data in self.mock_books]
        patched_book_query.all.return_value = mock_book_objects
        patched_book_json.return_value = {}

        result = Book.get_all_books()

        patched_book_query.all.assert_called_once()
        self.assertEqual(len(patched_book_json.mock_calls), len(self.mock_books))
        self.assertEqual(len(self.mock_books), len(result))

    def test_get_book(self):
        with patch.object(Book, 'query') as mock_query:

            mock_filter_by_result = Mock()
            mock_query.filter_by.return_value = mock_filter_by_result

            mock_first_result = Mock()
            mock_filter_by_result.first.return_value = mock_first_result

            mock_first_result.json.return_value = self.mock_books[0]

            fake_isbn = 'someisbn'

            Book.get_book(fake_isbn)

            mock_query.filter_by.assert_called_with(isbn=fake_isbn)
            mock_filter_by_result.first.assert_called_once()

    @patch.object(databases, 'session')
    @patch.object(Book, 'query')
    def test_delete_book(self, patched_query, patched_session):
        mock_filter_by = Mock()
        patched_query.filter_by.return_value = mock_filter_by
        mock_filter_by.delete.return_value = True

        isbn = 'fake_isbn'
        Book.delete_book(isbn)

        patched_query.filter_by.assert_called_with(isbn=isbn)
        mock_filter_by.delete.assert_called_once()
        patched_session.commit.assert_called_once()

    @patch.object(databases, 'session')
    @patch.object(Book, 'query')
    def test_update_book_price(self, patched_query, patched_session):

        # An alternative approach: test very lightly since the function is simple, just make sure the function
        # does not crash and commit is called once successfully

        isbn = 'fake_isbn'

        Book.update_book_price(isbn, 50)
        patched_query.filter_by.assert_called_once()
        patched_session.commit.assert_called_once()

    @patch.object(databases, 'session')
    @patch.object(Book, 'query')
    def test_update_book_name(self, patched_query, patched_session):
        isbn = 'fake_isbn'

        Book.update_book_name(isbn, 50)
        patched_session.commit.assert_called_once()

    @patch.object(databases, 'session')
    @patch.object(Book, 'query')
    def test_replace_book(self, patched_query, patched_session):

        Book.replace_book('some_isbn', 'somename', 50)
        patched_session.commit.assert_called_once()

        # Notice how this test is almost identical to the two tests above. This implies that the different functions
        # are actually doing the same things.
        # You could for example just write an "update_book_by_isbn" function that takes care of all these use cases.