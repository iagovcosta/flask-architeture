from functools import wraps
from flask import request
import string
import random
import jwt
from flask_architeture.models.user import User

random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(12))
SECRET_KEY = key


def user_by_username(name):
    try:
        return User.query.filter(User.name == name).one()
    except:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return {'message': 'É necessário o token de autenticação', 'data': {}}, 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = user_by_username(name=data['name'])
        except:
            return {'message': 'O token é inválido', 'data': {}}, 401
        return f(current_user, *args, **kwargs)
    return decorated
