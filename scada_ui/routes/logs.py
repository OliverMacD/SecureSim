import os
from flask import Blueprint, render_template, send_file
from scada_ui.auth import auth

logs_bp = Blueprint('logs', __name__)

@logs_bp.route("/logs")
@auth.login_required
def logs():
    return render_template("logs.html")

@logs_bp.route("/logs/live")
@auth.login_required
def get_logs():
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'logs.txt'))
    if os.path.exists(log_path):
        return send_file(log_path, mimetype="text/plain")
    return "Log file not found", 404
