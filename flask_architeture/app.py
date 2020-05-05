from flask import Flask, jsonify, request, send_file
from flask_architeture.extensions import configuration
from flask_architeture.extensions import database
from flask_architeture.extensions import migrations
from flask_architeture.extensions import views

from flask_marshmallow import Marshmallow

from werkzeug.utils import secure_filename
import datetime
import os

app = Flask(__name__)
configuration.init_app(app)

#configuracoes de upload
# # ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

db = database.init_app(app)
views.init_app(app, db)
migrations.init_app(app, db)

# ma = Marshmallow(app)

# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'name', 'email', 'password')

# class FileSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'name', 'user_id')


# user_schema = UserSchema()
# users_schemas = UserSchema(many=True)

# file_schema = FileSchema()
# files_schemas = FileSchema(many=True)
