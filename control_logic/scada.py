# control_logic/scada.py

import sys
import time
import json
from pymodbus.client import ModbusTcpClient
from pymodbus.server import ModbusServer
from process_sim.interfaces.mqtt_interface import subscribe_mqtt, init_mqtt

running = True

def load_layout():
    with open("example_layout.json") as f:
        return json.load(f)

def main():
    global running
    layout = load_layout()

    scada_config = layout["scada"]
    scada_ip = scada_config["ip"]
    scada_port = scada_config["port"]
    register_map = scada_config["register_map"]

    print(f"[SCADA] Starting on {scada_ip}:{scada_port}")
    init_mqtt()

    scada = ModbusServer(
        vendor_name="SecureSCADA",
        product_name="SCADA Controller",
        model="SCADA-1",
        revision="1.0",
        port=scada_port
    )
    scada.start()

    # Build device → PLC mapping
    device_plc_map = {}
    for plc in layout["plcs"]:
        for device in plc["devices"]:
            device_plc_map[device["id"]] = {
                "ip": plc["ip"],
                "port": plc["port"],
                "plc_reg": device["plc_input_register"]
            }

    def handle_kill(payload):
        global running
        if payload.lower() == "kill":
            print("[SCADA] Kill command received. Shutting down...")
            running = False

    subscribe_mqtt("scada/kill", handle_kill)

    try:
        while running:
            for device_id, scada_reg in register_map.items():
                plc_info = device_plc_map.get(device_id)
                if not plc_info:
                    continue

                try:
                    client = ModbusTcpClient(plc_info["ip"], port=plc_info["port"])
                    result = client.read_input_registers(plc_info["plc_reg"], 1)
                    client.close()
                    if result and not result.isError():
                        value = result.registers[0]
                        scada.set_holding_register(scada_reg, value)
                        print(f"[SCADA] {device_id} → HR[{scada_reg}] = {value}")
                except Exception as e:
                    print(f"[SCADA] Error reading {device_id}: {e}")

            time.sleep(2)
    except KeyboardInterrupt:
        pass

    print("[SCADA] Stopped.")

if __name__ == "__main__":
    main()
