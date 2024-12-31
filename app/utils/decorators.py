from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def recruiter_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'recruiter':
            flash('Accès non autorisé.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def candidate_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'candidate':
            flash('Accès non autorisé.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function