from flask import Blueprint
from .files_web import show_files, upload_file, delete_file, render_upload
from .users_web import render_register, create_user, render_update, render_login
# from flask_architeture.resources import au

bp = Blueprint("web", __name__, template_folder="templates")

#FILES
bp.add_url_rule("/files", view_func=show_files)
bp.add_url_rule("/files/delete/<int:id>", view_func=delete_file)
bp.add_url_rule("/files/upload", view_func=render_upload)
bp.add_url_rule("/files", methods=['POST'], view_func=upload_file)

#USERS
bp.add_url_rule("/register", view_func=render_register)
bp.add_url_rule("/user/register", view_func=create_user, methods=['POST'])
bp.add_url_rule("/user/update", view_func=render_update)
bp.add_url_rule("/login", view_func=render_login)

def init_app(app):
    app.register_blueprint(bp)