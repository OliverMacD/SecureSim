from control_logic.action_engine import ActionEngine


class SCADA:
    def __init__(self, config, graph, mqtt_interface):
        self.ip = config.get("ip")
        self.port = config.get("port")
        self.register_map = config.get("register_map", {})
        self.actions = config.get("actions", [])
        self.graph = graph
        self.engine = ActionEngine(self.register_map, self.graph, mqtt_interface)

    def update(self):
        for action in self.actions:
            self.engine.evaluate_and_execute(action)
