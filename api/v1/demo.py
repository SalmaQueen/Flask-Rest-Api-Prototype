from flask import jsonify, request, Response
import datetime
import jwt
from functools import wraps

import re

from api.v1.UserModel import User
from api.v1.BookModel import *

from api.__init__ import app
from api.v1.Utilities.validators import (valid_book_object,
                                         valid_put_request_data,
                                         valid_patch_request_data)


@app.route('/')
def homepage():
    """ The homepage route
    :return: A welcome message
    """
    return 'Welcome to Flask Rest API Prototype'


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json(force=True)
    username = str(request_data['username'])
    password = str(request_data['password'])

    if not username:
        response = jsonify({'error': 'Username is required'})
        response.status_code = 401
        return response

    elif not password:
        response = jsonify({'error': 'Password is required'})
        response.status_code = 401
        return response

    elif not re.match("^[a-zA-Z0-9_]*$", username):
        response = jsonify({'error': 'Username cannot contain special characters'})
        response.status_code = 400
        return response

    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = str(request.args.get('token'))
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}), 401

    return wrapper


# GET /books
@app.route('/books')
@token_required
def get_books():
    return jsonify({'books': Book.get_all_books()})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json(force=True)
    if valid_book_object(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 9780394800165 }"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json(force=True)
    if not valid_put_request_data(request_data):
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')
        return response
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if not valid_patch_request_data(request_data):
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')
        return response

    if "price" in request_data:
        Book.update_book_price(isbn, request_data['price'])
    if "name" in request_data:
        Book.update_book_name(isbn, request_data['name'])

    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# DELETE /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", status=204)
        return response
    invalid_book_object_error_msg = {
        "error": "Book with ISBN number provided not found, so unable to delete.",
    }
    response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype='application/json')
    return response


@app.route('/something')
@token_required
def something_that_needs_token():
    return jsonify({'msg': 'abc'})
