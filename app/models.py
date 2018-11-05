from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.Integer)
    author = db.Column(db.String(128))

    writeable_properties = ['price', 'name']

    def json(self):
        return {'name': self.name, 'price': self.price, 'isbn': self.isbn, 'author': self.author}

    @classmethod
    def update(cls, isbn, **kwargs):
        book = cls.query.filter_by(isbn=isbn).first()
        for key, value in kwargs.items():
            if key not in cls.writeable_properties:
                raise ValueError
            setattr(book, key, value)
        db.session.add(book)
        db.session.commit()

    @classmethod
    def add_book(cls, _name, _price, _isbn, _author):
        new_book = cls(name=_name, price=_price, isbn=_isbn, author=_author)
        db.session.add(new_book)
        db.session.commit()

    @classmethod
    def get_all_books(cls):
        return [cls.json(book) for book in cls.query.all()]

    @classmethod
    def get_book(cls, _isbn):
        book = cls.query.filter_by(isbn=_isbn).first()
        return book.json() if book else None

    @classmethod
    def delete_book(cls, _isbn):
        try:
            cls.query.filter_by(isbn=_isbn).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    def update_book_price(cls, _isbn, _price):
        book_to_update = cls.query.filter_by(isbn=_isbn).first()
        book_to_update.price = _price
        db.session.commit()

    @classmethod
    def update_book_name(cls, _isbn, _name):
        book_to_update = cls.query.filter_by(isbn=_isbn).first()
        book_to_update.name = _name
        db.session.commit()

    @classmethod
    def replace_book(cls, _isbn, _name, _price):
        book_to_replace = cls.query.filter_by(isbn=_isbn).first()
        if book_to_replace is not None:
            book_to_replace.price = _price
            book_to_replace.name = _name
            db.session.commit()

    def __repr__(self):
        return '<Book name={} isbn={} price={}>'.format(self.name, self.isbn, self.price)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

