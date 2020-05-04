from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATORS'] = False
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
    name = db.Column(db.String(200))
    directory = db.Column(db.String(200))
    user_id = db.Column(db.Integer())

    def __init__(self, id, name, directory, user_id):
        self.id = id
        self.name = name
        self.directory = directory
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

if __name__ == '__main__':
    app.run()