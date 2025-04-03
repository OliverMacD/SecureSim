# process_sim/pump.py

from process_sim.base import ProcessComponent
from process_sim.interfaces.mqtt_interface import publish_mqtt, subscribe_mqtt

class Pump(ProcessComponent):
    def __init__(self, id, name, rate, is_open=True):
        super().__init__(id, name)
        self.rate = rate
        self.source = None
        self.target = None
        self.is_open = is_open  # Default to open unless explicitly passed False

        # MQTT subscriptions
        subscribe_mqtt(f"get/pump/{self.id}/rate", self.handle_get_rate)
        subscribe_mqtt(f"set/pump/{self.id}/rate", self.handle_set_rate)
        subscribe_mqtt(f"get/pump/{self.id}/state", self.handle_get_state)
        subscribe_mqtt(f"set/pump/{self.id}/state", self.handle_set_state)

    # MQTT Handlers
    def handle_get_rate(self, _msg):
        publish_mqtt(f"state/pump/{self.id}/rate", self.rate)

    def handle_set_rate(self, msg):
        try:
            self.rate = float(msg)
        except ValueError:
            print(f"[Pump {self.id}] Invalid rate value: {msg}")

    def handle_get_state(self, _msg):
        state = "open" if self.is_open else "closed"
        publish_mqtt(f"state/pump/{self.id}/state", state)

    def handle_set_state(self, msg):
        if msg.lower() == "open":
            self.is_open = True
        elif msg.lower() == "closed":
            self.is_open = False
        else:
            print(f"[Pump {self.id}] Invalid state: {msg}")

    # Graph connection
    def set_connection(self, source_tank, line):
        self.source = source_tank
        self.target = line

    # Logic loop
    def update(self):
        if self.is_open and self.source and self.source.current_volume >= self.rate:
            self.source.current_volume -= self.rate
            self.target.transfer(self.rate)
        elif self.is_open and self.source and self.source.current_volume >= self.rate and self.source.current_volume > 0:
            self.source.current_volume = 0
            self.target.transfer(self.source.current_volume)

    def publish(self):
        publish_mqtt(f"pump/{self.id}/rate", self.rate)
        publish_mqtt(f"pump/{self.id}/state", "open" if self.is_open else "closed")

    # Optional local API
    def get_rate(self):
        return self.rate

    def set_rate(self, new_rate):
        self.rate = new_rate

    def get_state(self):
        return "open" if self.is_open else "closed"

    def set_state(self, state: str):
        self.is_open = state.lower() == "open"
