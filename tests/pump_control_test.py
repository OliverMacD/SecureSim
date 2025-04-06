# pump_control_test.py

import sys
import os
import time

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process_sim.interfaces.mqtt_interface import MQTTInterface

# Initialize MQTT client
client = MQTTInterface(broker="127.0.0.1", port=1883, client_id="test_client")

# Subscribe to pump state updates
client.subscribe("pump/pump1/state", lambda msg: print(f"[TEST] Received pump state: {msg}"))

# Wait until MQTT client is connected
while not client._connected:
    print("[TEST] Waiting for MQTT connection...")
    time.sleep(0.5)

# Keep the script running
print("[TEST] Listening for pump state...")
try:
    while True:
        client.publish("set/pump/pump1/state", "open")
        time.sleep(10)
except KeyboardInterrupt:
    print("\n[TEST] Stopped listening.")
