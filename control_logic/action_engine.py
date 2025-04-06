class ActionEngine:
    def __init__(self, register_map, graph, mqtt_interface):
        self.register_map = register_map  # maps device ids to registers
        self.graph = graph
        self.mqtt = mqtt_interface

    def evaluate_and_execute(self, action):
        trigger = action["trigger"]
        effect = action["effect"]

        reg = trigger["register"]
        cond = trigger["condition"]
        value = trigger["value"]

        # Find the device tied to this register
        device_id = self._resolve_device_id(reg)
        device = self.graph.nodes.get(device_id)

        # Skip if device not in graph
        if not device:
            print(f"[ENGINE] No device found for register {reg}")
            return

        current_val = self._get_value_from_device(device)

        if self._evaluate_condition(current_val, cond, value):
            self._execute_effect(effect)

    def _resolve_device_id(self, reg):
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
        if hasattr(device, "current_volume"):
            return device.current_volume
        elif hasattr(device, "get_state"):
            return 1 if device.get_state() == "open" else 0
        return 0

    def _evaluate_condition(self, actual, cond, expected):
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
            print(f"[ENGINE] Condition error: {e}")
        return False

    def _execute_effect(self, effect):
        targets = effect["target"]
        if not isinstance(targets, list):
            targets = [targets]

        for target_id in targets:
            if target_id == "scada":
                print(f"[SCADA ALERT]: {effect.get('message')}")
                continue

            node = self.graph.nodes.get(target_id)
            if not node:
                print(f"[ENGINE] No target found for {target_id}")
                continue

            action = effect.get("action")
            if hasattr(node, "set_state") and action in ["open", "close"]:
                node.set_state("open" if action == "open" else "closed")
                print(f"[ENGINE] Set state of {target_id} to {action}")
