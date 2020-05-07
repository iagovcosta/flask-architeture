from flask import abort, jsonify, request
from flask_restful import Resource
from flask_architeture.models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_architeture.bussines.auth.jwt_decorator import token_required 
import string
import random


class UserResource(Resource):

    @token_required
    def get(self):
        return User.get_delete_put_post()

    def post(self):
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        pass_hash = generate_password_hash(password)
        user = User(name, email, pass_hash)
        
        try:
            if user:
                db.session.add(user)
                db.session.commit()
                # result = user_schema.dump(user)
                # return {'message': 'Registrado com sucesso', 'data': user}, 201
                return {'message': 'Registrado com sucesso'}, 201
            else:
                return {'message': 'Não foi possível registrar', 'data': {}}, 500
        except:
            return {'message': 'Não foi possível registrar'}, 500

class UserItemResource(Resource):
    @token_required
    def get(self, id):
        try:
            return User.get_delete_put_post(id)
        except:
            return {'message': 'Nenhum usuário encontrado'}

    @token_required
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return {'message': 'Usuário não existe'}, 404

        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                # result = user_schema.dump(user)
                # return jsonify({'message': 'Usuário deletado', 'data': result}), 200
                return {'message': 'Usuário deletado'}, 200
            except:
                return {'message': 'Não foi possível deletar'}, 500

    @token_required
    def put(self, id):
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        user = User.query.get(id)

        if not user:
            return {'message': 'Usuário inexistente', 'data': {}}, 404

        pass_hash = generate_password_hash(password)

        try:
            user.name = name
            user.email = email
            user.password = pass_hash
            db.session.commit()
            # result = user_schema.dump(user)
            # return jsonify({'message': 'Usuário atualizado com sucesso', 'data': result}), 201
            return {'message': 'Usuário atualizado com sucesso'}, 201
        except:
            return {'message': 'Não foi possível atualizar o usuário', 'data': {}}, 500
