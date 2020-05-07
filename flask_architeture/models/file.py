from flask_architeture.extensions.database import db
from flask_serialize import FlaskSerializeMixin
from .soft_deletes import QueryWithSoftDelete
from .user import User
import datetime


class File(db.Model, FlaskSerializeMixin):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    path_file = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, server_onupdate=db.func.now())
    deleted = db.Column(db.Boolean(), default=False)

    query_class = QueryWithSoftDelete

    def __init__(self, name, path_file, user_id):
        self.name = name
        self.path_file = path_file
        self.user_id = user_id