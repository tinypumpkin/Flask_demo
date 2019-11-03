from flask import redirect,session,url_for
from functools import wraps

def valid(func):
    @wraps(func)
    def _valid(*args,**kwargs):
        if session.get('name'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("first_blue.login"))
    return _valid
