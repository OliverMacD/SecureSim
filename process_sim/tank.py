# process_sim/tank.py

from process_sim.base import ProcessComponent
from process_sim.interfaces.mqtt_interface import MQTTInterface

class Tank(ProcessComponent):
    def __init__(self, id, name, max_capacity, mqtt_interface: MQTTInterface):
        super().__init__(id, name)
        self.max_capacity = max_capacity
        self.current_volume = 0.0
        self.inputs = []
        self.outputs = []
        self.mqtt = mqtt_interface  # Injected instance of MQTTInterface

        # MQTT subscriptions
        self.mqtt.subscribe(f"set/tank/{self.id}/max_capacity", self.handle_set_max)

    def handle_set_max(self, msg):
        try:
            self.max_capacity = float(msg)
        except ValueError:
            print(f"[Tank {self.id}] Invalid max_capacity: {msg}")

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
        self.mqtt.publish(f"tank/{self.id}/volume", self.current_volume)
        self.mqtt.publish(f"tank/{self.id}/max_capacity", self.max_capacity)
        print(f"[Tank {self.id}] Published volume: {self.current_volume}, max_capacity: {self.max_capacity}")
        pass