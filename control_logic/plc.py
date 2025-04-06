from control_logic.action_engine import ActionEngine


class PLC:
    def __init__(self, plc_config, graph, mqtt_interface):
        self.id = plc_config["id"]
        self.ip = plc_config["ip"]
        self.port = plc_config["port"]
        self.devices = plc_config.get("devices", [])
        self.actions = plc_config.get("actions", [])
        self.graph = graph
        self.engine = ActionEngine(self.devices, self.graph, mqtt_interface)

    def update(self):
        for action in self.actions:
            self.engine.evaluate_and_execute(action)
