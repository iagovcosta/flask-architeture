from flask import abort, jsonify, request
from flask_restful import Resource
from flask_architeture.models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash

class UserResource(Resource):
    def get(self):
        return User.get_delete_put_post()

    def post(self):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        pass_hash = generate_password_hash(password)
        user = User(username=username, email=email, password=pass_hash)
        try:
            db.session.add(user)
            db.session.commit()
            # result = user_schema.dump(user)
            # return jsonify({'message': 'Registrado com sucesso', 'data': result}), 201
            return jsonify({'message': 'Registrado com sucesso'}), 201
        except:
            return jsonify({'message': 'Não foi possível registrar', 'data': {}}), 500

class UserItemResource(Resource):
    def get(self, id):
        user = User.query.get(id)

        if user:
            # result = user_schema.dump(user)
            # return jsonify({'message': 'Sucesso', 'data': result}), 201
            return jsonify({'message': 'Sucesso'}), 201

        return jsonify({'message': 'Usuário não existe', 'data': {}}), 404

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'Usuário não existe', 'data': {}}), 404

        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                # result = user_schema.dump(user)
                # return jsonify({'message': 'Usuário deletado', 'data': result}), 200
                return jsonify({'message': 'Usuário deletado'}), 200
            except:
                return jsonify({'message': 'Não foi possível deletar', 'data': {}}), 500

    def put(self, id):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        user = User.query.get(id)

        if not user:
            return jsonify({'message': 'Usuário inexistente', 'data': {}}), 404

        pass_hash = generate_password_hash(password)

        try:
            user.username = username
            user.email = email
            user.password = pass_hash
            db.session.commit()
            # result = user_schema.dump(user)
            # return jsonify({'message': 'Usuário atualizado com sucesso', 'data': result}), 201
            return jsonify({'message': 'Usuário atualizado com sucesso'}), 201
        except:
            return jsonify({'message': 'Não foi possível atualizar o usuário', 'data': {}}), 500
