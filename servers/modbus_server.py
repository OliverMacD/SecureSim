# servers/modbus_server.py

import logging
import threading
from modbus_tcp_server.network import ModbusTCPServer
from modbus_tcp_server.data_source import BaseDataSource

logging.basicConfig()
logger = logging.getLogger("modbus_server")
logger.setLevel(logging.INFO)


class CustomDataSource(BaseDataSource):
    def __init__(self, data, on_write=None):
        self.data = data
        self.on_write = on_write

    def get_holding_register(self, unit_id, address):
        return self.data[address]

    def set_holding_register(self, unit_id, address, value):
        self.data[address] = value
        if self.on_write:
            self.on_write(address, value)

    def get_analog_input(self, unit_id, address):
        return 0  # Not used

    def get_discrete_input(self, unit_id, address):
        return False  # Not used

    def get_coil(self, unit_id, address):
        return False  # Not used

    def set_coil(self, unit_id, address, value):
        pass  # Not used


class ModbusServerWrapper:
    def __init__(self, host='127.0.0.1', port=5020, initial_registers=None):
        """
        host: IP address to bind to
        port: TCP port
        initial_registers: dict of named registers (not used for now, just defines layout)
        """
        self.host = host
        self.port = port
        self.update_callback = None
        self.data = [0] * 100  # Holds 100 registers max by default
        self.data_source = CustomDataSource(self.data, self._on_change)
        self.server = ModbusTCPServer(bind_ifc=self.host, bind_port=self.port, data_source=self.data_source)

    def set_update_hook(self, callback_fn):
        """Called on every Modbus write."""
        self.update_callback = callback_fn
        self.data_source.on_write = self._on_change  # Update hook in data source

    def _on_change(self, address, value):
        if self.update_callback:
            self.update_callback(address, value)

    def read_register(self, address):
        return self.data[address]

    def write_register(self, address, value):
        self.data[address] = value
        self._on_change(address, value)

    def start(self):
        def run():
            logger.info(f"[MODBUS] Starting Modbus TCP server on {self.host}:{self.port}")
            self.server.run()
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        logger.info("[MODBUS] Modbus server launched.")
