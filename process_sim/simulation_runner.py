# process_sim/simulation_runner.py

import threading
import time
import logging
from process_sim.graph_visualizer import render_live_graph

class SimulationThread(threading.Thread):
    def __init__(self, graph, interval=1.0, debug=False):
        super().__init__()
        self.graph = graph
        self.interval = interval
        self.running = False
        self.debug = debug  # Debug flag enables visualizer

    def run(self):
        self.running = True
        logging.info("[SIM] Starting simulation loop...")

        # Optionally show non-blocking graph visualizer
        if self.debug:
            logging.info("[SIM] Debug mode: Starting live graph visualizer...")
            threading.Thread(target=lambda: render_live_graph(self.graph, self.interval), daemon=True).start()

        while self.running:
            start_time = time.time()

            self.graph.update()
            self.graph.publish()

            elapsed = time.time() - start_time
            sleep_time = max(0, self.interval - elapsed)
            time.sleep(sleep_time)

    def stop(self):
        self.running = False
        logging.info("[SIM] Stopping simulation loop...")
