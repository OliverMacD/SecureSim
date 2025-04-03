# process_sim/splitter.py

from process_sim.base import ProcessComponent
from process_sim.interfaces.mqtt_interface import publish_mqtt

class Splitter(ProcessComponent):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.outputs = []

    def add_output(self, line):
        self.outputs.append(line)

    def receive(self, amount):
        if not self.outputs:
            return
        split_amount = amount / len(self.outputs)
        for out in self.outputs:
            out.transfer(split_amount)

    def update(self):
        # Passive, only reacts to input
        pass

    def publish(self):
        publish_mqtt(f"splitter/{self.id}/status", f"{len(self.outputs)} outputs")
