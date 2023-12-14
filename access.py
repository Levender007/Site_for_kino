from flask import session, render_template, redirect, url_for, request, current_app
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('bp_auth.auth_index'))

    return wrapper


def group_validation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        endpoint_app = request.endpoint.split('.')[-1]
        config = current_app.config['access.json']
        if 'user_group' in session:
            user_group = session['user_group']
            if user_group in config and endpoint_app in config[user_group]:
                return func(*args, **kwargs)
            else:
                return render_template('forbidden.html')
        return func(*args, **kwargs)

    return wrapper
