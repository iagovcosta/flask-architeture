import jwt
import datetime
from werkzeug.security import check_password_hash
from flask import request, jsonify
from flask_restful import Resource
from functools import wraps
from flask_architeture.models.user import User
from .jwt_decorator import user_by_username

class Auth(Resource):
    def post(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return {'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}, 401
        
        user = user_by_username(auth.username)

        if not user:
            return {'message': 'Usuário não encontradp'}, 401

        if user and check_password_hash(user.password, auth.password):
            token = jwt.encode({'username': user.name, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12) }, '123')

            return {'message': 'Validated successfully', 'token': token.decode('UTF-8')}
        
        return {'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}, 401