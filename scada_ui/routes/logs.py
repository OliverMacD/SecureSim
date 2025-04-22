from flask import Blueprint, render_template
from scada_ui.auth import auth

logs_bp = Blueprint('logs', __name__)

@logs_bp.route("/logs")
@auth.login_required
def logs():
    return render_template("logs.html")