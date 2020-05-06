from flask import request, jsonify
from flask_architeture.models.user import User
from werkzeug.security import check_password_hash
from flask_restful import Resource
from functools import wraps
import string
import random
import datetime
import jwt

random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(12))
SECRET_KEY = key

class Auth(Resource):

    def user_by_username(self, name):
        try:
            return User.query.filter(User.name == name).one()
        except:
            return None

    def post(self):

        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return {'message': 'Acesso negado', 'WWW-Authenticate': 'Basic auth="Login necessário"'}, 401

        user = self.user_by_username(auth.username)
        if not user:
            return {'message': 'Usuário não encontrado', 'data': {}}, 401

        if user and check_password_hash(user.password, auth.password):
            token = jwt.encode({'name': user.name, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12)},
                               SECRET_KEY)
            return jsonify({'message': 'Validado com sucesso', 'token': token.decode('UTF-8'),
                            'exp': datetime.datetime.now() + datetime.timedelta(hours=12)})

        return {'message': 'Não foi possível verificar', 'WWW-Authenticate': 'Basic auth="Login necessário'}, 401