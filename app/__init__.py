from flask import Flask

from app.constants import HTTPStatusCodes
from app.controllers.v1 import v1
from app.errors import register_app_error_handlers
from app.extensions import db, migrate, jwt
from app.models import User
from app.request_hooks import register_request_hooks
from config import config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')

    register_extensions(app)
    register_app_error_handlers(app)
    register_blueprints(app)
    register_shell_context(app)
    register_request_hooks(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.authentication_handler(authenticate)
    jwt.identity_handler(get_identity)
    jwt.init_app(app)


def register_blueprints(app):
    app.register_blueprint(v1, url_prefix='/api/v1')


def register_shell_context(app):
    def shell_context():
        return dict()

    app.shell_context_processor(shell_context)


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user.verify_password(password):
        return user
    return None


def get_identity(payload):
    return User.query.filter_by(id=payload.get('identity')).first()

