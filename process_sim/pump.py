# process_sim/pump.py

from process_sim.base import ProcessComponent
from process_sim.interfaces.mqtt_interface import publish_mqtt, subscribe_mqtt

class Pump(ProcessComponent):
    def __init__(self, id, name, rate):
        super().__init__(id, name)
        self.rate = rate
        self.source = None
        self.target = None

        subscribe_mqtt(f"get/pump/{self.id}/rate", self.handle_get_rate)
        subscribe_mqtt(f"set/pump/{self.id}/rate", self.handle_set_rate)

    def handle_get_rate(self, _msg):
        publish_mqtt(f"state/pump/{self.id}/rate", self.rate)

    def handle_set_rate(self, msg):
        try:
            self.rate = float(msg)
        except ValueError:
            print(f"[Pump {self.id}] Invalid rate value: {msg}")

    def set_connection(self, source_tank, line):
        self.source = source_tank
        self.target = line

    def update(self):
        if self.source.current_volume >= self.rate:
            self.source.current_volume -= self.rate
            self.target.transfer(self.rate)

    def publish(self):
        publish_mqtt(f"pump/{self.id}/rate", self.rate)


    def get_rate(self):
        return self.rate

    def set_rate(self, new_rate):
        self.rate = new_rate
