from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATORS'] = False
db = SQLAlchemy(app)

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
    user_id = db.Column(db.Integer(10))

    def __init__(self, id, name, directory, user_id):
        self.id = id
        self.name = name
        self.directory = email
        self.user_id = user_id

@app.route('/')
def hello():
    # code
    return "Hello World!"

if __name__ == '__main__':
    app.run()