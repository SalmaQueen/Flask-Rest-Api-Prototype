
from flask import jsonify, request, Blueprint, abort, url_for
from flask_jwt import jwt_required

from app.models import Book
from app.utils import valid_book_object, valid_put_request_data, valid_patch_request_data

v1 = Blueprint('v1', __name__)


@v1.route('/')
def index():
    """ The homepage route
    :return: A welcome message
    """
    return 'Welcome to Flask Rest API Prototype'


@v1.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


@v1.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    if not valid_book_object(request.json):
        abort(400, "Invalid book object passed in request. Data passed in similar to this {'name': 'bookname', "
                   "'price': 7.99, 'isbn': 9780394800165, 'author': 'Someone' }")
    Book.add_book(request.json.get('name'), request.json.get('price'), request.json.get('isbn'), request.json.get('author'))
    data = dict(Location=url_for('v1.get_book_by_isbn', isbn=request.json.get('isbn')))
    return jsonify(data), 201


@v1.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    book = Book.get_book(isbn)
    if not book:
        abort(404, 'Book with isbn {} not found'.format(isbn))
    return jsonify(book)


@v1.route('/books/<int:isbn>', methods=['PUT'])
@jwt_required()
def replace_book(isbn):
    if not valid_put_request_data(request.json):
        abort(400, "Invalid book object passed in request. Data should be passed in similar to this {'name': "
                   "'bookname', 'price': 7.99 }")

    Book.replace_book(isbn, request.json.get('name'), request.json.get('price'))
    return jsonify(dict()), 204


@v1.route('/books/<int:isbn>', methods=['PATCH'])
@jwt_required()
def update_book(isbn):
    if not valid_patch_request_data(request.json):
        abort(400, "Invalid book object passed in request. Data should be passed in similar to this {'name': "
                   "'bookname', 'price': 7.99 }")

    Book.update(isbn, **request.json)

    return jsonify(dict(Location=url_for('v1.get_book_by_isbn', isbn=isbn))), 204


@v1.route('/books/<int:isbn>', methods=['DELETE'])
@jwt_required()
def delete_book(isbn):
    if not Book.delete_book(isbn):
        abort(404, "Book with ISBN number provided not found, so unable to delete.")
    return jsonify(dict()), 204
