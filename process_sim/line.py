# process_sim/line.py

from process_sim.base import ProcessComponent
from process_sim.interfaces.mqtt_interface import publish_mqtt

class Line(ProcessComponent):
    def __init__(self, id, name, source=None, target=None):
        super().__init__(id, name)
        self.source = source
        self.target = target
        self.buffer = 0.0

    def transfer(self, amount):
        self.buffer += amount

    def update(self):
        if self.target and self.buffer > 0:
            self.target.receive(self.buffer)
            self.buffer = 0.0

    def publish(self):
        publish_mqtt(f"line/{self.id}/flow", self.buffer)  # Flow rate if you have it
        publish_mqtt(f"line/{self.id}/buffer", self.buffer)
