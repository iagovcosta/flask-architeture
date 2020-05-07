from flask import request, render_template, jsonify, url_for, redirect, current_app
from flask_architeture.models.file import File, db
import datetime
import os 

def show_files():
    files = File.query.all()

    return render_template("files-list.html", files=files)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def upload_file():
    if 'file' not in request.files:
        return {'success': False, 'message': 'Nenhum arquivo enviado'}, 500

    file = request.files['file']

    if file.filename == '':
        return {'success': False, 'message': 'Nenhum arquivo enviado'}, 500

    if file and allowed_file(file.filename):
        hased_name = str(datetime.datetime.now().timestamp())+'.pdf'
            
        new_file = File(file.filename, hased_name, 1)

        db.session.add(new_file)
        db.session.commit()
            
        file.save(os.path.join('storage', hased_name))

        return redirect(url_for('web.show_files'))

def render_upload():
    return render_template('files-upload.html')

def delete_file(id):
    try:
        file = File.query.get(id)
        file.deleted = True

        db.session.commit()

        return redirect(url_for('web.show_files'))
    except:
        return jsonify({'sucess': False, 'message': 'Erro ao deletar'}), 404