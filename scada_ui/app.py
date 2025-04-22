import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import threading
import time
from flask import Flask
from scada_ui.routes.dashboard import dashboard_bp
from scada_ui.routes.logs import logs_bp
from scada_ui.routes.components import components_bp
from process_sim.layout_parser import load_layout
from process_sim.graph_visualizer import render_process_graph_to_file


def update_graph_loop():
    graph = load_layout("Process_sim.json")
    while True:
        render_process_graph_to_file(graph, output_path="scada_ui/static/img/graph.png")
        time.sleep(1)

def create_app():
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(components_bp)

    threading.Thread(target=update_graph_loop, daemon=True).start()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)