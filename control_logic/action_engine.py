"""
Action Engine

This module defines the ActionEngine class, which evaluates conditional rules (triggers)
based on register values and applies control effects to devices in the process graph.

Classes:
    ActionEngine - Executes logical actions using device states and a rule-based engine.
"""

import logging
import os

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

class ActionEngine:
    """
    A rule evaluation engine that enables PLC or SCADA systems to trigger actions
    based on register values mapped to simulation components.

    Attributes:
        register_map (dict or list): Mapping between device IDs and register addresses.
        graph (ProcessGraph): The simulation graph containing all components.
        mqtt (MQTTInterface): Optional communication layer for integration.
    """

    def __init__(self, register_map, graph, mqtt_interface):
        """
        Initializes the engine with a register map and graph reference.

        Args:
            register_map (dict or list): Mapping of register addresses to device IDs.
            graph (ProcessGraph): The simulation graph context.
            mqtt_interface (MQTTInterface): Interface for messaging (not used directly).
        """
        self.register_map = register_map
        self.graph = graph
        self.mqtt = mqtt_interface

    def evaluate_and_execute(self, action):
        """
        Evaluates a trigger condition and executes an effect if the condition is met.

        Args:
            action (dict): An action containing a "trigger" and "effect".
                Example:
                {
                    "trigger": {"register": 1, "condition": ">", "value": 50},
                    "effect": {"target": "pump1", "action": "open"}
                }
        """
        trigger = action["trigger"]
        effect = action["effect"]

        reg = trigger["register"]
        cond = trigger["condition"]
        value = trigger["value"]

        device_id = self._resolve_device_id(reg)
        device = self.graph.nodes.get(device_id)

        if not device:
            logging.info(f"[ENGINE] No device found for register {reg}")
            return

        current_val = self._get_value_from_device(device)

        if self._evaluate_condition(current_val, cond, value):
            self._execute_effect(effect)

    def _resolve_device_id(self, reg):
        """
        Resolves the device ID from a given register number.

        Args:
            reg (int): Register number to match.

        Returns:
            str or None: Corresponding device ID or None if not found.
        """
        if isinstance(self.register_map, dict):
            for k, v in self.register_map.items():
                if v == reg:
                    return k
        elif isinstance(self.register_map, list):
            for entry in self.register_map:
                if entry.get("plc_input_register") == reg:
                    return entry["id"]
        return None

    def _get_value_from_device(self, device):
        """
        Extracts the current value from a simulation device.

        Args:
            device (ProcessComponent): A tank, pump, or similar component.

        Returns:
            float or int: The current state or reading of the device.
        """
        if hasattr(device, "current_volume"):
            return device.current_volume
        elif hasattr(device, "get_state"):
            return 1 if device.get_state() == "open" else 0
        return 0

    def _evaluate_condition(self, actual, cond, expected):
        """
        Compares an actual value to an expected value using a condition operator.

        Args:
            actual (float or int): Measured value.
            cond (str): Comparison operator as a string (e.g., "==", ">", "<=").
            expected (float or int): Threshold or value to compare against.

        Returns:
            bool: Result of the condition.
        """
        try:
            if cond == "==":
                return actual == expected
            elif cond == "!=":
                return actual != expected
            elif cond == ">":
                return actual > expected
            elif cond == "<":
                return actual < expected
            elif cond == ">=":
                return actual >= expected
            elif cond == "<=":
                return actual <= expected
        except Exception as e:
            logging.info(f"[ENGINE] Condition error: {e}")
        return False

    def _execute_effect(self, effect):
        """
        Executes the defined effect on a target or targets.

        Args:
            effect (dict): Contains "target" (str or list), "action" (e.g., "open"), and optionally "message".
        """
        targets = effect["target"]
        if not isinstance(targets, list):
            targets = [targets]

        for target_id in targets:
            if target_id == "scada":
                logging.info(f"[SCADA ALERT]: {effect.get('message')}")
                continue

            node = self.graph.nodes.get(target_id)
            if not node:
                logging.info(f"[ENGINE] No target found for {target_id}")
                continue

            action = effect.get("action")
            if hasattr(node, "set_state") and action in ["open", "close"]:
                node.set_state("open" if action == "open" else "closed")
                logging.info(f"[ENGINE] Set state of {target_id} to {action}")
