import jwt
from flask import request
from functools import wraps
from flask_architeture.models.user import User

def user_by_username(username):
    try:
        return User.query.filter(User.name == username).one()
    except:
        return None

def token_required(f):
        @wraps(f)
        def decorated(self, *args, **kwargs):
            token = request.args.get('token')

            if not token:
                return {'message': 'token não informado'}, 401

            try:
                data = jwt.decode(token, '123')
                current_user = user_by_username(data['username'])
            except:
                return {'message': 'Token inválido'}, 401

            return f(current_user, *args, **kwargs)

        return decorated