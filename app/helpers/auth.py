from functools import wraps

from flask import request, abort, current_app


def require_auth(fn):
    @wraps(fn)
    def check_token(*args, **kwargs):
        token = request.headers.get('X-Chatsubo-Token')
        if not token:
            abort(401)
            return

        if not token == current_app.config["auth_token"]:
            abort(401)
        else:
            return fn(*args, **kwargs)

    return check_token
