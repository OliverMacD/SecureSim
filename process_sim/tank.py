"""
Tank Component

Represents a fluid tank in the process simulation. Tracks volume and capacity,
handles MQTT-based configuration, and supports data publishing for SCADA or monitoring systems.

Classes:
    Tank - Manages fluid input, capacity constraints, and MQTT interactions.
"""

from process_sim.base import ProcessComponent
from process_sim.interfaces.mqtt_interface import MQTTInterface

class Tank(ProcessComponent):
    """
    Tank node that stores fluid volume. Can receive input from connected lines and
    report status via MQTT. Maximum capacity is configurable remotely.
    """

    def __init__(self, id, name, max_capacity, mqtt_interface: MQTTInterface):
        """
        Args:
            id (str): Unique identifier for the tank.
            name (str): Human-readable name.
            max_capacity (float): Maximum volume the tank can hold.
            mqtt_interface (MQTTInterface): Interface for MQTT messaging.
        """
        super().__init__(id, name)
        self.max_capacity = max_capacity
        self.current_volume = 0.0
        self.inputs = []
        self.outputs = []
        self.mqtt = mqtt_interface

        # Listen for remote capacity adjustments
        self.mqtt.subscribe(f"set/tank/{self.id}/max_capacity", self.handle_set_max)

    def handle_set_max(self, msg):
        """
        Handle incoming MQTT messages to update the tank's maximum capacity.

        Args:
            msg (str): New maximum capacity as a string (parsed as float).
        """
        try:
            self.max_capacity = float(msg)
        except ValueError:
            print(f"[Tank {self.id}] Invalid max_capacity: {msg}")

    def add_input(self, line):
        """Registers an incoming connection line."""
        self.inputs.append(line)

    def add_output(self, line):
        """Registers an outgoing connection line."""
        self.outputs.append(line)

    def receive(self, amount):
        """
        Accepts incoming fluid, constrained by the tank's max capacity.

        Args:
            amount (float): Volume to add.
        """
        overflow = max(0, self.current_volume + amount - self.max_capacity)
        self.current_volume = min(self.current_volume + amount, self.max_capacity)

        if overflow > 0:
            # Log overflow event
            self.mqtt.publish(f"tank/{self.id}/overflow", overflow)
            print(f"[Tank {self.id}] Overflow detected: {overflow} units lost.")
    
    def transfer(self, amount):
        """
        Adds fluid to the tank, ensuring it does not exceed max_capacity.

        Args:
            amount (float): The amount of fluid to transfer.
        """
        if amount < 0:
            raise ValueError("Transfer amount cannot be negative.")
        
        self.current_volume = min(self.current_volume + amount, self.max_capacity)
        print(f"[Tank {self.id}] Transferred {amount} units. Current volume: {self.current_volume}")
        

    def output(self):
        """
        Returns the current volume. Used in flow calculations.

        Returns:
            float: Current stored volume.
        """
        return self.current_volume

    def update(self):
        """No periodic logic required for tanks, reserved for future use."""
        pass

    def publish(self):
        """
        Publishes current tank state (volume and max capacity) to MQTT topics.
        """
        self.mqtt.publish(f"tank/{self.id}/volume", self.current_volume)
        self.mqtt.publish(f"tank/{self.id}/max_capacity", self.max_capacity)
        print(f"[Tank {self.id}] Published volume: {self.current_volume}, max_capacity: {self.max_capacity}")
