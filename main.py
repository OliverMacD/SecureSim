"""
Main Entry Point for Process Simulation

This script launches and manages the simulation environment. It starts the MQTT broker,
loads the system layout, runs the simulation loop, and launches the Flask-based dashboard.

Functions:
    launch_flask() - Launches the Flask dashboard in a background thread.
    start_mqtt_server() - Starts the MQTT broker as a subprocess.
    wait_for_broker() - Waits for the MQTT broker to become available.
    main() - Orchestrates the full simulation launch sequence.
"""

from process_sim.layout_parser import load_layout
from process_sim.simulation_runner import SimulationThread
from scada_ui.services import sim_ref
import os
import sys
import time
import logging
import socket
import subprocess
import threading
import argparse
from attacks.Replay import capture_and_replay

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

# Test logging
logging.info("Logger initialized successfully")

"""
    Parses command-line arguments using argparse library
"""
def parse_arguments():
    parser = argparse.ArgumentParser(prog="Main", description="Executes the SecureSim simulation")

    parser.add_argument("-r", "--replay", action="store_true", help="Enable replay attack") # Replay attack
    parser.add_argument("--replay-time", type=int, default=10, help="Sets the replay attack's duration (ONLY USE WITH REPLAY ARGUMENT)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enables debug mode")

    return parser.parse_args()

def launch_flask():
    """
    Launch the Flask dashboard UI in a background subprocess.

    Assumes Flask app is located at `scada_ui/app.py`.
    """

    subprocess.Popen(
        ["python", "scada_ui/app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
    print("[MAIN] Flask dashboard launched at http://localhost:5000")

def start_mqtt_server():
    """
    Start the MQTT broker as a subprocess.

    Returns:
        subprocess.Popen: The running MQTT broker process, or None on failure.
    """
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
    """
    Blocks until the MQTT broker is reachable or timeout is exceeded.

    Args:
        host (str): Broker host address.
        port (int): Broker port.
        timeout (float): Max time to wait in seconds.

    Returns:
        bool: True if broker becomes available, False if timed out.
    """
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


def main(args):
    """
    Main simulation launcher. This function:
      1. Starts the MQTT broker
      2. Waits for the broker to be ready
      3. Loads the process layout
      4. Starts the simulation engine
      5. Launches the Flask dashboard
      6. Waits for keyboard interrupt to shut down
    """
  
    # Debug level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

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
    
    # REPLAY ATTACK
    # Currently uses capture_and_replay command, see attacks/Replay.py for the other two
    # I think switching this to use the two separate commands would be better
    # since if there is captured data already (from previous process simulation run),
    # then that data can simply be used
    if args.replay:
        logging.info("[MAIN] Starting replay attack...")
        threading.Thread(target=lambda: capture_and_replay(capture_time=args.replay_time), daemon=True).start()

    # Step 3: Load layout and start simulation
    print("[MAIN] Loading layout...")
    try:
        graph = load_layout("Process_sim.json")
        sim_ref.graph = graph  # Connect live simulation graph to UI
    except Exception as e:
        logging.error(f"[MAIN] Failed to load layout: {e}")
        mqtt_process.terminate()
        return

    print("[MAIN] Starting simulation...")
    sim_thread = SimulationThread(graph, interval=1.0, debug=False)
    sim_thread.start()

    # Step 4: Launch Flask dashboard
    print("[MAIN] Launching Flask dashboard...")
    threading.Thread(target=launch_flask, daemon=True).start()

    # Step 5: Wait for shutdown
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
    args = parse_arguments()
    main(args)
