from importlib import import_module
from dynaconf import FlaskDynaconf

def load_extensions(app):
    for extension in app.config.get('EXTENSIONS'):
        mod = import_module(extension)
        mod.init_app(app)

def load_extensions_db(app, db):
    for extension in app.config.get('EXTENSIONS_DB'):
        mod = import_module(extension)
        mod.init_app(app, db)

def init_app(app):
    FlaskDynaconf(app)