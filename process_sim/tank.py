# process_sim/tank.py

from process_sim.base import ProcessComponent
from process_sim.interfaces.mqtt_interface import publish_mqtt, subscribe_mqtt

class Tank(ProcessComponent):
    def __init__(self, id, name, max_capacity):
        super().__init__(id, name)
        self.max_capacity = max_capacity
        self.current_volume = 0.0
        self.inputs = []
        self.outputs = []

        subscribe_mqtt(f"get/tank/{self.id}/max_capacity", self.handle_get_max)
        subscribe_mqtt(f"set/tank/{self.id}/max_capacity", self.handle_set_max)
        subscribe_mqtt(f"get/tank/{self.id}/current_capacity", self.handle_get_current)

    def handle_get_max(self, _msg):
        publish_mqtt(f"state/tank/{self.id}/max_capacity", self.max_capacity)

    def handle_set_max(self, msg):
        try:
            self.max_capacity = float(msg)
        except ValueError:
            print(f"[Tank {self.id}] Invalid max_capacity: {msg}")

    def handle_get_current(self, _msg):
        publish_mqtt(f"state/tank/{self.id}/current_capacity", self.current_volume)

    def add_input(self, line):
        self.inputs.append(line)

    def add_output(self, line):
        self.outputs.append(line)

    def receive(self, amount):
        self.current_volume = min(self.current_volume + amount, self.max_capacity)

    def output(self):
        return self.current_volume  # This would normally control flow

    def update(self):
        # Placeholder: update logic if necessary
        pass

    def publish(self):
        publish_mqtt(f"tank/{self.id}/volume", self.current_volume)
        publish_mqtt(f"tank/{self.id}/max_capacity", self.max_capacity)
