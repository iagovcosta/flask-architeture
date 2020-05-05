from flask import abort, jsonify, request
from flask_restful import Resource
from flask_architeture.models.file import File, db

import datetime
import os


class FileResource(Resource):
    def get(self):
        return File.get_delete_put_post()

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    def post(self):
        if 'file' not in request.files:
            return {'success': False, 'message': 'Nenhuma imagem enviada'}

        file = request.files['file']

        if file.filename == '':
            return {'success': False, 'message': 'Nenhuma imagem enviada'}

        if file and self.allowed_file(file.filename):
            hased_name = str(datetime.datetime.now().timestamp())+'.pdf'
            
            new_file = File(file.filename, hased_name, 1)
            db.session.add(new_file)
            db.session.commit()
            
            file.save(os.path.join('storage', hased_name))

            return {'success': True, 'message': 'Arquivo salvo com sucesso'}


class FileItemResource(Resource):
    def delete(self, file_id):
        try:
            file = File.query.get(file_id)
            file.deleted = True
            
            db.session.commit()

            return {'success': True}, 200
        except:
            return {'success': False, 'message': 'Erro ao excluir'}, 404

    def get(self, file_id):
        try:
            return File.get_delete_put_post(file_id)
        except:
            return {'success': False, 'message': 'Arquivo não encontrado!'}, 404