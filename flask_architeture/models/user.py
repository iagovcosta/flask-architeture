from flask_architeture.extensions.database import db
from flask_serialize import FlaskSerializeMixin
from flask_sqlalchemy import BaseQuery
from .soft_deletes import QueryWithSoftDelete
import datetime

class User(db.Model, FlaskSerializeMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    files = db.relationship('File', backref='users_id')

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
