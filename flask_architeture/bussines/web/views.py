from flask import request, render_template, jsonify, url_for, redirect
from flask_architeture.models.file import File, db
import datetime
import os

def init_app(app, db):
    @app.route('/files', methods=['GET'])
    def showFiles():
        files = File.query.all()

        return render_template("files-list.html", files=files)

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

    @app.route('/files/delete/<int:id>', methods=['GET'])
    def delete_user(id):
        try:
            file = File.query.get(id)

            file.deleted = True
            
            db.session.commit()

            return redirect(url_for('showFiles'))
        except:
            return jsonify({'sucess': False, 'message': 'Erro ao deletar'}), 404






    @app.route('/test', methods=['GET'])
    def teste():
        return render_template('login.html')