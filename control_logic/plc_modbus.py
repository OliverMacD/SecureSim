"""
Modbus PLC Controller

This module extends the standard PLC to include Modbus TCP support, enabling
external systems to interact with simulated devices via register reads and writes.

Classes:
    ModbusPLC - A PLC that exposes device states via a Modbus TCP server.
"""

# Add the root directory of the project to the Python path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from control_logic.plc import PLC
from servers.modbus_server import ModbusServerWrapper


class ModbusPLC(PLC):
    """
    A Programmable Logic Controller (PLC) with Modbus TCP integration.

    In addition to evaluating control actions, this class serves a Modbus interface
    to synchronize device states and accept overrides from external tools.

    Attributes:
        modbus_registers (dict): Mapping of device IDs to Modbus register addresses.
        modbus (ModbusServerWrapper): Embedded Modbus TCP server instance.
    """

    def __init__(self, plc_config, graph, mqtt_interface):
        """
        Initializes the ModbusPLC and starts the Modbus TCP server.

        Args:
            plc_config (dict): Configuration for the PLC including devices and Modbus setup.
            graph (ProcessGraph): The full simulation graph.
            mqtt_interface (MQTTInterface): Communication interface for internal messaging.
        """
        super().__init__(plc_config, graph, mqtt_interface)
        self.modbus_registers = {dev["id"]: dev["plc_input_register"] for dev in plc_config["devices"]}
        self.modbus = ModbusServerWrapper(
            host=plc_config.get("ip", "127.0.0.1"),
            port=plc_config.get("port", 5100),
            initial_registers=self.modbus_registers
        )
        self.modbus.set_update_hook(self.on_register_write)
        self.modbus.start()

    def update(self):
        """
        Executes PLC logic and pushes device states to Modbus registers.
        Called once per simulation cycle.
        """
        super().update()
        self.push_data_to_registers()

    def push_data_to_registers(self):
        """
        Writes the state of each device to its corresponding Modbus register.
        """
        for device in self.devices:
            dev_id = device["id"]
            reg = device["plc_input_register"]
            sim_obj = self.graph.nodes.get(dev_id)
            if not sim_obj:
                continue

            if hasattr(sim_obj, "current_volume"):
                value = int(sim_obj.current_volume)
            elif hasattr(sim_obj, "get_state"):
                value = 1 if sim_obj.get_state() == "open" else 0
            else:
                value = 0

            self.modbus.write_register(reg, value)

    def on_register_write(self, address, value):
        """
        Callback triggered when a Modbus register is written externally.

        Updates the corresponding simulation object with the new value.

        Args:
            address (int): Modbus register address.
            value (int or float): New value written to the register.
        """
        for device in self.devices:
            if device["plc_input_register"] == address:
                dev_id = device["id"]
                sim_obj = self.graph.nodes.get(dev_id)

                if not sim_obj:
                    continue

                # Apply the value to the simulated object
                if hasattr(sim_obj, "set_state"):
                    sim_obj.set_state("open" if value == 1 else "closed")
                elif hasattr(sim_obj, "set_rate"):
                    sim_obj.set_rate(value)
                elif hasattr(sim_obj, "current_volume"):
                    sim_obj.current_volume = float(value)
                elif hasattr(sim_obj, "max_capacity"):
                    sim_obj.max_capacity = float(value)

                print(f"[MODBUS-PLC] Overwrote {dev_id} at register {address} with value {value}")
