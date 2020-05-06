from flask import Flask, jsonify, request, send_file
from flask_architeture.extensions import configuration
from flask_architeture.extensions.database import db, init_app
from flask_architeture.extensions import migrations
from flask_architeture.bussines import views
from flask_architeture.bussines import resources

app = Flask(__name__)

configuration.init_app(app)
init_app(app) #database_factory
migrations.init_app(app, db)
resources.init_app(app)

views.init_app(app, db)
