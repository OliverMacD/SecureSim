import json
from flask import Blueprint, render_template, jsonify
from scada_ui.services.graph_state import get_modbus_state
from scada_ui.auth import auth

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/")
@auth.login_required
def dashboard():
    return render_template("dashboard.html")

@dashboard_bp.route("/api/state")
@auth.login_required
def api_state():
    # Poll the Process_sim.json to understand how many pumps and tanks exist
    with open('Process_sim.json', 'r') as f:
        layout = json.load(f)

    # Extract pumps and tanks from the JSON
    pumps = {pump['id']: pump for pump in layout['nodes'] if pump['type'] == 'Pump'}
    tanks = {tank['id']: tank for tank in layout['nodes'] if tank['type'] == 'Tank'}

    # Create a mapping of pumps and tanks to their current state via Modbus
    state = {}

    # Add pump states to the state dictionary
    for pump_id, pump in pumps.items():
        pump_state = get_modbus_state(f"pump/{pump_id}/state")  # Fetch the state using MQTT
        state[pump_id] = {'name': pump['name'], 'state': pump_state, 'rate': pump['flow_rate']}

    # Add tank states to the state dictionary
    for tank_id, tank in tanks.items():
        tank_state = get_modbus_state(f"tank/{tank_id}/volume")  # Fetch the volume using MQTT
        state[tank_id] = {'name': tank['name'], 'volume': tank_state}

    return jsonify(state)
