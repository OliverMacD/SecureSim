from process_sim.layout_parser import load_layout
from process_sim.simulation_runner import SimulationThread
from process_sim.interfaces.mqtt_interface import init_mqtt
import time
import logging

def main():
    logging.basicConfig(level=logging.INFO)

    init_mqtt()  # Start MQTT broker client
    graph = load_layout("example_layout.json")

    # Run simulation with debug=True to enable live graph visualizer
    sim_thread = SimulationThread(graph, interval=1.0, debug=True)
    sim_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        sim_thread.stop()
        sim_thread.join()

if __name__ == "__main__":
    main()
