# process_sim/pump.py

from process_sim.base import ProcessComponent
from process_sim.interfaces.mqtt_interface import MQTTInterface

class Pump(ProcessComponent):
    def __init__(self, id, name, rate, mqtt_interface: MQTTInterface, is_open=True):
        super().__init__(id, name)
        self.rate = rate
        self.source = None
        self.target = None
        self.is_open = is_open
        self.mqtt = mqtt_interface  # Injected instance of MQTTInterface

        # MQTT subscriptions
        self.mqtt.subscribe(f"set/pump/{self.id}/rate", self.handle_set_rate)
        self.mqtt.subscribe(f"set/pump/{self.id}/state", self.handle_set_state)

    def handle_set_rate(self, msg):
        try:
            self.rate = float(msg)
        except ValueError:
            print(f"[Pump {self.id}] Invalid rate value: {msg}")

    def handle_set_state(self, msg):
        print(f"[Pump {self.id}] Received set_state command: {msg}")
        if msg.lower() == "open":
            self.is_open = True
        elif msg.lower() == "closed":
            self.is_open = False
        else:
            print(f"[Pump {self.id}] Invalid state: {msg}")
            return

        # Confirm new state over MQTT
        self.mqtt.publish(f"state/pump/{self.id}/state", "open" if self.is_open else "closed")
        print(f"[Pump {self.id}] State set to {self.is_open}")

    # Graph connection
    def set_connection(self, source_tank, line):
        self.source = source_tank
        self.target = line

    # Logic loop
    def update(self):
        if self.is_open and self.source and self.source.current_volume >= self.rate:
            self.source.current_volume -= self.rate
            self.target.transfer(self.rate)
        elif self.is_open and self.source and self.source.current_volume > 0:
            # Transfer remaining volume if less than rate
            self.target.transfer(self.source.current_volume)
            self.source.current_volume = 0

    def publish(self):
        self.mqtt.publish(f"pump/{self.id}/rate", self.rate)
        self.mqtt.publish(f"pump/{self.id}/state", "open" if self.is_open else "closed")
        print(f"[Pump {self.id}] Published rate: {self.rate}, state: {'open' if self.is_open else 'closed'}")

    # Optional local API
    def get_rate(self):
        return self.rate

    def set_rate(self, new_rate):
        self.rate = new_rate

    def get_state(self):
        return "open" if self.is_open else "closed"

    def set_state(self, state: str):
        self.is_open = state.lower() == "open"
