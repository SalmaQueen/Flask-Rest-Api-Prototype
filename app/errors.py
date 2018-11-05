from flask import jsonify

from app.utils import get_class_members
from app.constants import HTTPStatusCodes


def register_app_error_handlers(app):
    for _, code in get_class_members(HTTPStatusCodes):
        # Skip if code is not an error
        if code < 400:
            continue

        @app.errorhandler(code)
        def handler(error, status_code=code):
            return jsonify(dict(code=error.code, message=error.description)), status_code
