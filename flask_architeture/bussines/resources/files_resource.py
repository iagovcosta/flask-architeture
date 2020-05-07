from flask import abort, jsonify, request
from flask_restful import Resource
from flask_architeture.models.file import File, db
from flask_architeture.bussines.auth.jwt_decorator import token_required

import datetime
import os


class FileResource(Resource):
    @token_required
    def get(self):
        return File.get_delete_put_post()

    @token_required
    def post(self, current_user):
        if 'file' not in request.files:
            return {'success': False, 'message': 'Nenhuma imagem enviada'}, 500

        file = request.files['file']

        if file.filename == '':
            return {'success': False, 'message': 'Nenhuma imagem enviada'}, 500

        allowed_file = '.' in file.filename and \
            file.filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

        if file and allowed_file:
            hased_name = str(datetime.datetime.now().timestamp())+'.pdf'

            new_file = File(file.filename, hased_name, current_user.user_id)
            db.session.add(new_file)
            db.session.commit()
            
            file.save(os.path.join('storage', hased_name))

            return {'success': True, 'message': 'Arquivo salvo com sucesso'}, 200


class FileItemResource(Resource):
    @token_required
    def delete(self, file_id):
        try:
            file = File.query.get(file_id)
            file.deleted = True
        
            db.session.commit()

            return {'success': True}, 200
        except:
            return {'success': False, 'message': 'Erro ao excluir'}, 500

    @token_required
    def get(self, file_id):
        try:
            return File.get_delete_put_post(file_id)
        except:
            return {'success': False, 'message': 'Arquivo não encontrado!'}, 404