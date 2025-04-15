import json
from flask import Blueprint, render_template

components_bp = Blueprint('components', __name__)

@components_bp.route("/components")
def components():
    with open('Process_sim.json', 'r') as f:
        layout = json.load(f)
    return render_template("components.html", nodes=layout["nodes"])