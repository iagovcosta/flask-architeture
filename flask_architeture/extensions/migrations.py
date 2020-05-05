from flask_migrate import Migrate

migration = Migrate()

def init_app(app, db):
    migration.init_app(app, db)