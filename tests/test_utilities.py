import unittest

from app.utils import valid_book_object, valid_patch_request_data, valid_put_request_data


class TestValidators(unittest.TestCase):

    def test_valid_book_object_true(self):
        valid = valid_book_object({'name': 'abc', 'price': 50, 'isbn': 34242})
        self.assertTrue(valid)

    def test_valid_book_object_with_set(self):
        valid = valid_book_object({'name', 'price', 'isbn'})
        self.assertFalse(valid)

    def test_valid_book_object_invalid(self):
        valid = valid_book_object({'name': 'abc', 'price': 30})
        self.assertFalse(valid)

    def test_valid_put_object_true(self):
        valid = valid_put_request_data({'name': 'abc', 'price': 50})
        self.assertTrue(valid)

    def test_valid_put_object_with_set(self):
        valid = valid_put_request_data({'name', 'price'})
        self.assertFalse(valid)

    def test_valid_put_object_invalid(self):
        valid = valid_put_request_data({'name': 'abc'})
        self.assertFalse(valid)

    def test_valid_patch_object_true(self):
        valid = valid_patch_request_data({'name': 'abc'})
        self.assertTrue(valid)

    def test_valid_patch_object_with_set(self):
        valid = valid_patch_request_data({'name'})
        self.assertFalse(valid)

    def test_valid_patch_object_invalid(self):
        valid = valid_patch_request_data(dict())
        self.assertFalse(valid)





