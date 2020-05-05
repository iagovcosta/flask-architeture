from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
import datetime
import os

app = Flask(__name__)

#configuracoes de upload
UPLOAD_FOLDER = 'storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.deleted else None

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    path_file = db.Column(db.String(255))
    user_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, server_onupdate=db.func.now())
    deleted = db.Column(db.Boolean(), default=False)

    query_class = QueryWithSoftDelete

    def __init__(self, name, path_file, user_id):
        self.name = name
        self.path_file = path_file
        self.user_id = user_id

    def to_dict(self):
        return {'id': self.id, 'message': self.message,
                'url': url_for('get_message', id=self.id),
                'user_url': url_for('get_user', id=self.user_id)
                if not self.user.deleted else None}

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')

class FileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'user_id')


user_schema = UserSchema()
users_schemas = UserSchema(many=True)

file_schema = FileSchema()
files_schemas = FileSchema(many=True)

@app.route('/')
def hello():
    all_users = User.query.all()
    result = users_schemas.dump(all_users)
    return jsonify(result)

@app.route('/files', methods=['GET'])
def showFiles():
    all_files = File.query.all()
    result = files_schemas.dump(all_files)

    return jsonify({'files': result})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
