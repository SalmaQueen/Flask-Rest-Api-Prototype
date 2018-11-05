from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

from api.__init__ import databases


class Book(databases.Model):
    __tablename__ = 'books'
    id = databases.Column(databases.Integer, primary_key=True)
    name = databases.Column(databases.String(80), nullable=False)
    price = databases.Column(databases.Float, nullable=False)
    isbn = databases.Column(databases.Integer)

    def json(self):
        return {'name': self.name, 'price': self.price, 'isbn': self.isbn}

    @classmethod
    def add_book(cls, _name, _price, _isbn):
        new_book = cls(name=_name, price=_price, isbn=_isbn)
        databases.session.add(new_book)
        databases.session.commit()

    @classmethod
    def get_all_books(cls):
        return [cls.json(book) for book in cls.query.all()]

    @classmethod
    def get_book(cls, _isbn):
        book = cls.query.filter_by(isbn=_isbn).first()
        if book is not None:
            return cls.json(book)
        return {}

    @classmethod
    def delete_book(cls, _isbn):
        is_successful = cls.query.filter_by(isbn=_isbn).delete()
        databases.session.commit()
        return bool(is_successful)

    @classmethod
    def update_book_price(cls, _isbn, _price):
        book_to_update = cls.query.filter_by(isbn=_isbn).first()
        book_to_update.price = _price
        databases.session.commit()

    @classmethod
    def update_book_name(cls, _isbn, _name):
        book_to_update = cls.query.filter_by(isbn=_isbn).first()
        book_to_update.name = _name
        databases.session.commit()

    @classmethod
    def replace_book(cls, _isbn, _name, _price):
        book_to_replace = cls.query.filter_by(isbn=_isbn).first()
        if book_to_replace is not None:
            book_to_replace.price = _price
            book_to_replace.name = _name
            databases.session.commit()

    def __repr__(self):
        book_object = {
            'name': self.name,
            'price': self.price,
            'isbn': self.isbn
        }
        return json.dumps(book_object)
