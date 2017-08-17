import jwt
from functools import wraps
from flask import request
from app import User, Session, app


# Token based authentication decorator.

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return {
                       'message': 'Token is missing! Please login.'
                   }, 401
        try:
            token_data = jwt.decode(token, app.config['SECRET'])

            session_exist = Session.query.filter_by(user_id=token_data['public_id'], token=token).first()

            if not session_exist:
                return {
                           'message': 'You are not logged in. Please login!!!'
                       }, 403

            current_user = User.query.filter_by(public_id=token_data['public_id']).first()
        except:
            return {
                       'message': 'Token is invalid! Please login.'
                   }, 401

        return func(current_user, *args, **kwargs)

    return decorated
