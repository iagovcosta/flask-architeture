from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, send_file
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from io import BytesIO

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    data = db.Column(db.String(255))
    user_id = db.Column(db.Integer())

    def __init__(self, name, data, user_id):
        self.name = name
        self.data = data
        self.user_id = user_id

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')

class FileSchema(ma.Schema):
    class Meta:
        fields = ('name', 'directory', 'user_id')


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

@app.route('/files', methods=['POST'])
def uploadFiles():

    file_request = request.files['file']

    new_file = File(file_request.filename, file_request.read(), 1)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/files/download')
def downloadFiles():
    file_data = File.query.filter_by(id=1).first()

    return send_file(BytesIO(file_data.data), attachment_filename='flask.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run()