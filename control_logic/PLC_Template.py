# control_logic/plc_template.py

import sys
import time
import json
from pymodbus.server import ModbusServer
from process_sim.interfaces.mqtt_interface import subscribe_mqtt, init_mqtt

running = True

def load_layout():
    with open("example_layout.json") as f:
        return json.load(f)

def main():
    global running
    if len(sys.argv) < 2:
        print("Usage: python plc_template.py <plc_id>")
        return

    plc_id = sys.argv[1]
    layout = load_layout()
    plc_info = next((p for p in layout["plcs"] if p["id"] == plc_id), None)

    if not plc_info:
        print(f"[PLC] PLC ID '{plc_id}' not found in layout.")
        return

    ip = plc_info["ip"]
    port = plc_info["port"]

    print(f"[PLC-{plc_id}] Starting on {ip}:{port}")
    init_mqtt()

    plc = ModbusServer(
        vendor_name="SecurePLC",
        product_name="PLC Controller",
        model=f"PLC-{plc_id}",
        revision="1.0",
        port=port
    )
    plc.start()

    for device in plc_info["devices"]:
        reg = device["plc_input_register"]
        topic = device["mqtt_topic"]
        device_id = device["id"]

        def make_cb(address=reg, dev=device_id):
            def cb(payload):
                try:
                    value = int(json.loads(payload).get("value", 0))
                    plc.set_input_register(address, value)
                    print(f"[PLC-{plc_id}] {dev} → IR[{address}] = {value}")
                except Exception as e:
                    print(f"[PLC-{plc_id}] Error in {dev}: {e}")
            return cb

        subscribe_mqtt(topic, make_cb())

    def handle_kill(payload):
        global running
        if payload.lower() == "kill":
            print(f"[PLC-{plc_id}] Kill command received.")
            running = False

    subscribe_mqtt(f"{plc_id}/kill", handle_kill)

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    print(f"[PLC-{plc_id}] Stopped.")

if __name__ == "__main__":
    main()
