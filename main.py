from process_sim.layout_parser import load_layout
from process_sim.simulation_runner import SimulationThread
import os
import sys
import time
import logging
import socket
import subprocess
import threading

def launch_flask():
    """Launch the Flask Dashboard in a separate subprocess."""
    dashboard_path = os.path.join(os.path.dirname(__file__), "scada_ui", "Dashboard.py")
    subprocess.Popen(
        ["python", "scada_ui/app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
    print("[MAIN] Flask dashboard launched at http://localhost:5000")

def start_mqtt_server():
    """Start the MQTT server as a subprocess."""
    try:
        process = subprocess.Popen(
            ["python", "servers/mqtt_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process
    except Exception as e:
        logging.error(f"Failed to start MQTT server: {e}")
        return None

def wait_for_broker(host="127.0.0.1", port=1883, timeout=5.0):
    """Wait for the MQTT broker to be ready."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                logging.info("[MAIN] MQTT broker is ready.")
                return True
        except Exception:
            time.sleep(0.2)
    logging.error("[MAIN] MQTT broker did not respond in time.")
    return False

def main():
    logging.basicConfig(level=logging.INFO)

    # Step 1: Start MQTT Broker subprocess
    mqtt_process = start_mqtt_server()
    if not mqtt_process:
        logging.error("[MAIN] Failed to start MQTT broker. Exiting.")
        return
    logging.info("[MAIN] MQTT broker starting...")

    # Step 2: Wait until broker is accepting connections
    if not wait_for_broker():
        logging.error("[MAIN] Failed to connect to MQTT broker. Exiting.")
        mqtt_process.terminate()
        return

    # Step 4: Load layout and start simulation
    print("[MAIN] Loading layout...")
    try:
        graph = load_layout("Process_sim.json")
    except Exception as e:
        logging.error(f"[MAIN] Failed to load layout: {e}")
        mqtt_process.terminate()
        return

    print("[MAIN] Starting simulation...")
    sim_thread = SimulationThread(graph, interval=1.0, debug=True)
    sim_thread.start()

    # Launch Streamlit in background
    print("[MAIN] Launching Flask dashboard...")
    threading.Thread(target=launch_flask, daemon=True).start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logging.info("[MAIN] Stopping simulation...")
        sim_thread.stop()
        sim_thread.join()
        mqtt_process.terminate()
        logging.info("[MAIN] MQTT broker stopped.")

if __name__ == "__main__":
    main()
