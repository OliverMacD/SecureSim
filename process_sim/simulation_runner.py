"""
Simulation Runner

This module defines a threaded simulation controller that orchestrates the update
cycle for process components, PLCs, SCADA systems, and optional live visualization.

Classes:
    SimulationThread - Main thread for managing and updating the entire simulation.
"""

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

# Ensure the 'data' directory exists
log_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(log_dir, exist_ok=True)

# Set full path to log file inside data/
log_path = os.path.join(log_dir, "logs.txt")

# Reset logging if needed
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Setup logging to file
logging.basicConfig(
    level=logging.INFO,
    filename=log_path,
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Optional: Console output to debug
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger().addHandler(console)

class SimulationThread(threading.Thread):
    """
    Main simulation thread that updates the entire system at a fixed time interval.
    This includes:
      - MQTT communication setup
      - PLC and SCADA updates
      - Process component updates
      - Optional real-time graph visualization
    """

    def __init__(self, graph, interval=1.0, debug=False):
        """
        Args:
            graph (ProcessGraph): The simulation graph (nodes and lines).
            interval (float): Time (in seconds) between simulation ticks.
            debug (bool): Enables live graph visualization if True.
        """
        super().__init__()
        self.graph = graph
        self.interval = interval
        self.running = False
        self.debug = debug

        # Initialize shared MQTT interface
        self.mqtt = MQTTInterface(client_id="sim_control")

        # Initialize control systems
        self.plcs = [ModbusPLC(plc_config, graph, self.mqtt) for plc_config in graph.plc_configs]
        self.scada = ModbusSCADA(graph.scada_config, graph, self.mqtt) if graph.scada_config else None

    def run(self):
        """
        Main loop of the simulation thread. Updates control logic, the process graph,
        and handles optional real-time visualization. Maintains a consistent tick rate.
        """
        self.running = True
        logging.info("[SIM] Starting simulation loop...")

        if self.debug:
            logging.info("[SIM] Debug mode: Starting live graph visualizer...")
            threading.Thread(target=lambda: render_live_graph(self.graph, self.interval), daemon=True).start()

        while self.running:
            start_time = time.time()

            # Update PLCs
            for plc in self.plcs:
                plc.update()

            # Update SCADA if present
            if self.scada:
                self.scada.update()

            # Update process graph and publish values
            self.graph.update()
            self.graph.publish()

            # Sleep to maintain fixed update rate
            elapsed = time.time() - start_time
            sleep_time = max(0, self.interval - elapsed)
            time.sleep(sleep_time)

    def stop(self):
        """
        Stops the simulation loop on the next iteration.
        """
        self.running = False
        logging.info("[SIM] Stopping simulation loop...")
