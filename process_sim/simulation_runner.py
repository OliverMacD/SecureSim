# process_sim/simulation_runner.py

# Add the root directory of the project to the Python path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import threading
import time
import logging

from process_sim.graph_visualizer import render_live_graph
from control_logic.plc_modbus import ModbusPLC
from control_logic.scada_modbus import ModbusSCADA
from process_sim.interfaces.mqtt_interface import MQTTInterface


class SimulationThread(threading.Thread):
    def __init__(self, graph, interval=1.0, debug=False):
        super().__init__()
        self.graph = graph
        self.interval = interval
        self.running = False
        self.debug = debug  # Debug flag enables visualizer

        # Init MQTT shared instance
        self.mqtt = MQTTInterface(client_id="sim_control")

        # Use Modbus-enhanced control logic
        self.plcs = [ModbusPLC(plc_config, graph, self.mqtt) for plc_config in graph.plc_configs]
        self.scada = ModbusSCADA(graph.scada_config, graph, self.mqtt) if graph.scada_config else None

    def run(self):
        self.running = True
        logging.info("[SIM] Starting simulation loop...")

        # Optionally show non-blocking graph visualizer
        if self.debug:
            logging.info("[SIM] Debug mode: Starting live graph visualizer...")
            threading.Thread(target=lambda: render_live_graph(self.graph, self.interval), daemon=True).start()

        while self.running:
            start_time = time.time()

            # Update logic controllers
            for plc in self.plcs:
                plc.update()
            if self.scada:
                self.scada.update()

            # Update and publish process graph
            self.graph.update()
            self.graph.publish()

            # Maintain consistent tick rate
            elapsed = time.time() - start_time
            sleep_time = max(0, self.interval - elapsed)
            time.sleep(sleep_time)

    def stop(self):
        self.running = False
        logging.info("[SIM] Stopping simulation loop...")
