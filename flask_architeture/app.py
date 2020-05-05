from flask import Flask, jsonify, request, send_file
from flask_architeture.extensions import configuration
from flask_architeture.extensions.database import db, init_app
from flask_architeture.extensions import migrations
from flask_architeture.views import views

app = Flask(__name__)
configuration.init_app(app)

init_app(app)
migrations.init_app(app, db)

views.init_app(app, db)
