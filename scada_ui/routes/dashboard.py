import json
from flask import Blueprint, render_template, jsonify
from scada_ui.services.graph_state import get_modbus_state

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/")
def dashboard():
    return render_template("dashboard.html")

@dashboard_bp.route("/api/state")
def api_state():
    # Poll the Process_sim.json to understand how many pumps and tanks exist
    with open('Process_sim.json', 'r') as f:
        layout = json.load(f)

    # Extract pumps and tanks from the JSON
    pumps = {pump['id']: pump for pump in layout['nodes'] if pump['type'] == 'Pump'}
    tanks = {tank['id']: tank for tank in layout['nodes'] if tank['type'] == 'Tank'}

    # Create a mapping of pumps and tanks to their current state via Modbus
    state = {}

    for pump_id, pump in pumps.items():
        pump_state = get_modbus_state(f"pump/{pump_id}/state")  # Custom function to get pump state via Modbus
        state[pump_id] = {'state': pump_state, 'rate': pump['flow_rate']}

    for tank_id, tank in tanks.items():
        tank_state = get_modbus_state(f"tank/{tank_id}/volume")  # Custom function to get tank volume via Modbus
        state[tank_id] = {'volume': tank_state}

    return jsonify(state)
