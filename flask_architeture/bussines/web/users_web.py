from flask import abort, jsonify, request, render_template, redirect, url_for
from flask_restful import Resource
from flask_architeture.models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import string
import random


def render_register():
    return render_template('register.html')

def list_users():
    return User.get_delete_put_post()

def render_update():
    return render_template('user-update.html')

def render_login():
    return render_template('login.html')

def create_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    pass_hash = generate_password_hash(password)
    user = User(name, email, pass_hash)
    if user:
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    else:
        return {'message': 'Não foi possível registrar', 'data': {}}, 500


def get_user(id):
    user = User.query.get(id)

    if user:
        return {'message': 'Sucesso'}, 201

    return jsonify({'message': 'Usuário não existe', 'data': {}}), 404

def delete_user(id):
    user = User.query.get(id)
    if not user:
        return {'message': 'Usuário não existe', 'data': {}}, 404

    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'Usuário deletado'}, 200
        except:
            return {'message': 'Não foi possível deletar', 'data': {}}, 500

def update_user(id):
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
        return {'message': 'Usuário atualizado com sucesso'}, 201
    except:
        return {'message': 'Não foi possível atualizar o usuário', 'data': {}}, 500
