"""
PLC Controller

This module defines a simple Programmable Logic Controller (PLC) abstraction.
Each PLC evaluates and executes logic rules over a defined set of devices using the ActionEngine.

Classes:
    PLC - A control unit that operates over assigned devices using rule-based logic.
"""

from control_logic.action_engine import ActionEngine


class PLC:
    """
    Programmable Logic Controller (PLC) for localized control of process devices.

    Evaluates predefined logic actions on associated devices and triggers control operations.

    Attributes:
        id (str): Unique identifier for the PLC.
        ip (str): IP address assigned to the PLC.
        port (int): Listening port for the PLC (for simulation context).
        devices (list): List of device IDs under the PLC's control.
        actions (list): Rule-based logic expressions to be evaluated.
        graph (ProcessGraph): Reference to the process simulation graph.
        engine (ActionEngine): Engine used to evaluate and apply control actions.
    """

    def __init__(self, plc_config, graph, mqtt_interface):
        """
        Initializes the PLC with its configuration, control scope, and logic engine.

        Args:
            plc_config (dict): Configuration dictionary including 'id', 'ip', 'port', 'devices', and 'actions'.
            graph (ProcessGraph): The simulation graph containing all components.
            mqtt_interface (MQTTInterface): Communication interface for live updates.
        """
        self.id = plc_config["id"]
        self.ip = plc_config["ip"]
        self.port = plc_config["port"]
        self.devices = plc_config.get("devices", [])
        self.actions = plc_config.get("actions", [])
        self.graph = graph
        self.engine = ActionEngine(self.devices, self.graph, mqtt_interface)

    def update(self):
        """
        Executes all configured control actions using the action engine.
        Called once per simulation cycle.
        """
        for action in self.actions:
            self.engine.evaluate_and_execute(action)
