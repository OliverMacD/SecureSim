"""
Modbus SCADA Controller

Extends the SCADA system with Modbus TCP integration for real-time data synchronization
between simulation components and external Modbus clients.

Classes:
    ModbusSCADA - A SCADA interface enhanced with Modbus TCP server support.
"""

# Add the root directory of the project to the Python path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from control_logic.scada import SCADA
from servers.modbus_server import ModbusServerWrapper


class ModbusSCADA(SCADA):
    """
    SCADA controller with Modbus support.

    Publishes selected component data to Modbus registers and allows external writes
    to control simulated process components.

    Attributes:
        register_map (dict): Mapping of device IDs to Modbus register addresses.
        modbus (ModbusServerWrapper): Embedded Modbus TCP server instance.
    """

    def __init__(self, scada_config, graph, mqtt_interface):
        """
        Initializes ModbusSCADA and starts the Modbus TCP server.

        Args:
            scada_config (dict): SCADA configuration dictionary.
            graph (ProcessGraph): Process simulation graph.
            mqtt_interface (MQTTInterface): Interface for MQTT communication.
        """
        super().__init__(scada_config, graph, mqtt_interface)
        self.register_map = scada_config.get("register_map", {})
        self.modbus = ModbusServerWrapper(
            host=scada_config.get("ip", "127.0.0.1"),
            port=scada_config.get("port", 5200),
            initial_registers=self.register_map
        )
        self.modbus.set_update_hook(self.on_register_write)
        self.modbus.start()

    def update(self):
        """
        Executes SCADA logic and pushes updated simulation values to Modbus registers.
        """
        super().update()
        self.push_data_to_registers()

    def push_data_to_registers(self):
        """
        Writes current state of mapped simulation objects to Modbus holding registers.
        """
        for dev_id, reg in self.register_map.items():
            sim_obj = self.graph.nodes.get(dev_id)
            if not sim_obj:
                continue

            if hasattr(sim_obj, "current_volume"):
                value = int(sim_obj.current_volume)
            elif hasattr(sim_obj, "get_state"):
                value = 1 if sim_obj.get_state() == "open" else 0
            elif hasattr(sim_obj, "get_rate"):
                value = int(sim_obj.get_rate())
            else:
                value = 0

            self.modbus.write_register(reg, value)

    def on_register_write(self, address, value):
        """
        Callback for external Modbus register writes. Applies the written value
        to the mapped simulation object.

        Args:
            address (int): The register address that was written.
            value (int or float): The new value written to the register.
        """
        for dev_id, reg in self.register_map.items():
            if reg == address:
                sim_obj = self.graph.nodes.get(dev_id)
                if not sim_obj:
                    continue

                if hasattr(sim_obj, "set_state"):
                    sim_obj.set_state("open" if value == 1 else "closed")
                elif hasattr(sim_obj, "set_rate"):
                    sim_obj.set_rate(value)
                elif hasattr(sim_obj, "current_volume"):
                    sim_obj.current_volume = float(value)
                elif hasattr(sim_obj, "max_capacity"):
                    sim_obj.max_capacity = float(value)

                print(f"[MODBUS-SCADA] Overwrote {dev_id} at register {address} with value {value}")
