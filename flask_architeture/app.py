from flask import Flask, jsonify, request, send_file
from flask_architeture.extensions import configuration
from flask_architeture.extensions.database import db, init_app
from flask_architeture.extensions import migrations
from flask_architeture.extensions import bootstrap
from flask_architeture.bussines import web
from flask_architeture.bussines import resources

import string
import random



app = Flask(__name__)


random_str = string.ascii_letters + string.digits +string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(12))
app.config['SECRET_KEY'] = key 

configuration.init_app(app)
init_app(app) #database_factory
migrations.init_app(app, db)
resources.init_app(app)
bootstrap.init_app(app)
web.init_app(app)
# views.init_app(app, db)
