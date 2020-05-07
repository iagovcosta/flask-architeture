from flask_architeture.extensions.database import db
from flask_serialize import FlaskSerializeMixin
from flask_sqlalchemy import BaseQuery
from .soft_deletes import QueryWithSoftDelete
import datetime

class User(db.Model, FlaskSerializeMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200))
    files = db.relationship('File', backref='users_id')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
