from process_sim.layout_parser import load_layout
from process_sim.simulation_runner import SimulationThread
from process_sim.interfaces.mqtt_interface import init_mqtt
import subprocess
import time
import logging
import os
import sys
import socket

def start_mqtt_server():
    path = os.path.join("servers", "mqtt_server.py")
    return subprocess.Popen([sys.executable, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def wait_for_broker(host="localhost", port=1883, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                print("[MAIN] MQTT broker is ready.")
                return True
        except Exception:
            time.sleep(0.2)
    print("[MAIN] MQTT broker did not respond in time.")
    return False

def main():
    logging.basicConfig(level=logging.INFO)

    # Step 1: Start MQTT Broker subprocess
    mqtt_process = start_mqtt_server()
    print("[MAIN] MQTT broker starting...")

    # Step 2: Wait until broker is accepting connections
    if not wait_for_broker():
        print("[MAIN] Failed to connect to MQTT broker. Exiting.")
        mqtt_process.terminate()
        return

    # Step 3: Initialize MQTT client
    init_mqtt()

    # Step 4: Load layout and start simulation
    graph = load_layout("example_layout.json")
    sim_thread = SimulationThread(graph, interval=1.0, debug=False)
    sim_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("[MAIN] Stopping simulation...")
        sim_thread.stop()
        sim_thread.join()
        mqtt_process.terminate()
        print("[MAIN] MQTT broker stopped.")

if __name__ == "__main__":
    main()
