from flask import redirect, request


def register_request_hooks(app):
    @app.before_request
    def redirect_http():
        if not app.config.get('DEBUG') and request.headers.get('X-Forwarded-Proto') != 'https':
            return redirect(request.url.replace('http://', 'https://', 1), code=301)
