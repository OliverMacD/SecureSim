"""
Modbus TCP Server Wrapper

This module defines a lightweight Modbus TCP server using the `modbus_tcp_server` package.
It supports reading and writing to holding registers and allows a user-defined callback
to be triggered on register writes.

Classes:
    CustomDataSource - Handles Modbus register access and optionally triggers a callback on writes.
    ModbusServerWrapper - Manages the Modbus server and exposes a simplified interface
                          for integration with simulation or control systems.
"""

import logging
import threading
import os
from modbus_tcp_server.network import ModbusTCPServer
from modbus_tcp_server.data_source import BaseDataSource

logging.basicConfig()
logger = logging.getLogger("modbus_server")
logger.setLevel(logging.INFO)

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

class CustomDataSource(BaseDataSource):
    """
    Custom Modbus data source providing access to holding registers and supporting
    write callbacks for integration with external logic.
    """

    def __init__(self, data, on_write=None):
        """
        Args:
            data (list): List of register values.
            on_write (callable, optional): Callback triggered on register write.
        """
        self.data = data
        self.on_write = on_write

    def get_holding_register(self, unit_id, address):
        return self.data[address]

    def set_holding_register(self, unit_id, address, value):
        self.data[address] = value
        if self.on_write:
            self.on_write(address, value)

    def get_analog_input(self, unit_id, address):
        return 0  # Not implemented

    def get_discrete_input(self, unit_id, address):
        return False  # Not implemented

    def get_coil(self, unit_id, address):
        return False  # Not implemented

    def set_coil(self, unit_id, address, value):
        pass  # Not implemented


class ModbusServerWrapper:
    """
    Wrapper around a ModbusTCPServer that provides register read/write
    access and supports user-defined write hooks.
    """

    def __init__(self, host='127.0.0.1', port=5020, initial_registers=None):
        """
        Args:
            host (str): IP address to bind the server.
            port (int): Port number to listen on.
            initial_registers (dict): Optional named register definitions (not currently used).
        """
        self.host = host
        self.port = port
        self.update_callback = None
        self.data = [0] * 100  # Default size of 100 holding registers
        self.data_source = CustomDataSource(self.data, self._on_change)
        self.server = ModbusTCPServer(bind_ifc=self.host, bind_port=self.port, data_source=self.data_source)

    def set_update_hook(self, callback_fn):
        """
        Registers a callback function to be called whenever a register is written.

        Args:
            callback_fn (callable): Function with signature callback(address, value)
        """
        self.update_callback = callback_fn
        self.data_source.on_write = self._on_change

    def _on_change(self, address, value):
        if self.update_callback:
            self.update_callback(address, value)

    def read_register(self, address):
        """
        Returns the value of a register.

        Args:
            address (int): Register address

        Returns:
            int: Register value
        """
        return self.data[address]

    def write_register(self, address, value):
        """
        Writes a value to a register and triggers the write callback.

        Args:
            address (int): Register address
            value (int): Value to write
        """
        self.data[address] = value
        self._on_change(address, value)

    def start(self):
        """
        Starts the Modbus server in a separate daemon thread.
        """
        def run():
            logger.info(f"[MODBUS] Starting Modbus TCP server on {self.host}:{self.port}")
            self.server.run()

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        logger.info("[MODBUS] Modbus server launched.")
