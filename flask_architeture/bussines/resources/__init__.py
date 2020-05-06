from flask import Blueprint
from flask_restful import Api
from .files_resource import FileResource, FileItemResource
from .user_resource import UserResource, UserItemResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")

api = Api(bp)
api.add_resource(FileResource, "/file")
api.add_resource(FileItemResource, "/file/<file_id>")
api.add_resource(UserResource, "/user")
api.add_resource(UserItemResource, "/user/<id>")

def init_app(app):
    app.register_blueprint(bp)