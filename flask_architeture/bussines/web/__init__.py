from flask import Blueprint
from .files_web import show_files, upload_file, delete_file, render_upload

bp = Blueprint("web", __name__, template_folder="templates")

#FILES
bp.add_url_rule("/files", view_func=show_files)
bp.add_url_rule("/files/delete/<int:id>", view_func=delete_file)
bp.add_url_rule("/files/upload", view_func=render_upload)
bp.add_url_rule("/files", methods=['POST'], view_func=upload_file)

#USERS

def init_app(app):
    app.register_blueprint(bp)