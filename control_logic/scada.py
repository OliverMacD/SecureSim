"""
SCADA Interface

This module defines a lightweight SCADA controller that evaluates and executes
high-level actions on a process graph based on a predefined register map.

Classes:
    SCADA - Supervisory control component that manages and applies system-wide logic.
"""

from control_logic.action_engine import ActionEngine


class SCADA:
    """
    Supervisory Control and Data Acquisition (SCADA) class.

    Uses a provided configuration to evaluate and execute actions across
    the process graph using the ActionEngine.

    Attributes:
        ip (str): Optional IP address for external interfaces.
        port (int): Optional port number.
        register_map (dict): Mapping of register names to process components.
        actions (list): List of SCADA action rules to evaluate.
        engine (ActionEngine): Evaluates and executes actions.
    """

    def __init__(self, config, graph, mqtt_interface):
        """
        Initializes the SCADA system with configuration and graph context.

        Args:
            config (dict): Dictionary containing SCADA setup info.
            graph (ProcessGraph): The full simulation graph.
            mqtt_interface (MQTTInterface): MQTT interface used by the ActionEngine.
        """
        self.ip = config.get("ip")
        self.port = config.get("port")
        self.register_map = config.get("register_map", {})
        self.actions = config.get("actions", [])
        self.graph = graph
        self.engine = ActionEngine(self.register_map, self.graph, mqtt_interface)

    def update(self):
        """
        Executes all configured SCADA actions using the action engine.
        Called once per simulation cycle.
        """
        for action in self.actions:
            self.engine.evaluate_and_execute(action)
