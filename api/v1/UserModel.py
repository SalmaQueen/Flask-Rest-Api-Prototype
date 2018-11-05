from flask_sqlalchemy import SQLAlchemy

from api.__init__ import app, databases

db = SQLAlchemy(app)


class User(databases.Model):
    __tablename__ = 'users'
    id = databases.Column(databases.Integer, primary_key=True)
    username = databases.Column(databases.String(80), unique=True, nullable=False)
    password = databases.Column(databases.String(80), nullable=False)



    @classmethod
    def createUser(cls, _username, _password):
        new_user = User(username=_username, password=_password)
        databases.session.add(new_user)
        databases.session.commit()

    @classmethod
    def getAllUsers(cls):
        return User.query.all()


    def __repr__(self):
        return str({
            'username': self.username,
            'password': self.password
        })

    def username_password_match(_username, _password):
        user = User.query.filter_by(username=_username).filter_by(password=_password).first()
        if user is None:
            return False
        else:
            return True



