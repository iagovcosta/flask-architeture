from flask import request, jsonify, abort
from flask_architeture.models.models import File, User
import datetime
import os

def init_app(app, db):
    @app.route('/')
    def hello():
        all_users = User.query.all()
        return jsonify(all_users)

    @app.route('/files', methods=['GET'])
    def showFiles():
        # files = File.query.all() or abort(204)

        return File.get_delete_put_post()
        # return jsonify(
        #     {"files": [file.to_dict() for file in files]}
        # )

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    @app.route('/files', methods=['POST'])
    def uploadFiles():
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'Nenhuma imagem enviada'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'success': False, 'message': 'Nenhuma imagem enviada'})

        if file and allowed_file(file.filename):
            hased_name = str(datetime.datetime.now().timestamp())+'.pdf'
            
            new_file = File(file.filename, hased_name, 1)
            db.session.add(new_file)
            db.session.commit()
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], hased_name))

            return jsonify({'success': True, 'message': 'Arquivo salvo com sucesso'})

    @app.route('/files/<int:id>', methods=['DELETE'])
    def delete_user(id):
        file = File.query.get_or_404(id)
        file.deleted = True
        
        db.session.commit()

        return jsonify({'sucess': True, 'message': 'Deletado com sucesso'}), 204