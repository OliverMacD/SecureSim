"""
Pump Component

Represents a controllable pump in the simulation. Transfers fluid from a source tank
to a connected line. Supports MQTT for setting and reporting state and rate.

Classes:
    Pump - Handles input/output flow, remote control, and MQTT publishing.
"""

from process_sim.base import ProcessComponent
from process_sim.interfaces.mqtt_interface import MQTTInterface
from process_sim.splitter import Splitter
from process_sim.tank import Tank 

class Pump(ProcessComponent):
    """
    A pump that transfers fluid at a fixed rate from a source tank to a target line.
    The pump can be remotely opened or closed and configured via MQTT.
    """

    def __init__(self, id, name, rate, mqtt_interface: MQTTInterface, is_open=True):
        """
        Args:
            id (str): Unique identifier.
            name (str): Human-readable name.
            rate (float): Flow rate (units per tick).
            mqtt_interface (MQTTInterface): Communication interface.
            is_open (bool): Initial state of the pump (True if open).
        """
        super().__init__(id, name)
        self.rate = rate
        self.source = None
        self.target = None
        self.is_open = is_open
        self.mqtt = mqtt_interface

        # Listen for external control messages
        self.mqtt.subscribe(f"set/pump/{self.id}/rate", self.handle_set_rate)
        self.mqtt.subscribe(f"set/pump/{self.id}/state", self.handle_set_state)

    def handle_set_rate(self, msg):
        """
        Handles incoming MQTT message to change pump rate.

        Args:
            msg (str): New rate value (float as string).
        """
        try:
            self.rate = float(msg)
            print(f"[Pump {self.id}] Rate set to: {self.rate}")
        except ValueError:
            print(f"[Pump {self.id}] Invalid rate value: {msg}")

    def handle_set_state(self, msg):
        """
        Handles MQTT message to open or close the pump.

        Args:
            msg (str): Expected to be 'open' or 'closed'.
        """
        print(f"[Pump {self.id}] Received set_state command: {msg}")
        if msg.lower() == "open":
            self.is_open = True
        elif msg.lower() == "closed":
            self.is_open = False
        else:
            print(f"[Pump {self.id}] Invalid state: {msg}")
            return

        self.mqtt.publish(f"state/pump/{self.id}/state", "open" if self.is_open else "closed")
        print(f"[Pump {self.id}] State set to {'open' if self.is_open else 'closed'}")

    def set_connection(self, source_tank, target_tank, line):
        """
        Defines the source and target connections for the pump.

        Args:
            source_tank (Tank): Source tank supplying fluid.
            target_tank (Tank): Target tank receiving fluid.
            line (Line): Output line where fluid is transferred.
        """
        self.source = source_tank
        self.target = target_tank

    def update(self):
        """
        Transfers fluid from the source tank to the target if the pump is open.
        Handles both Tank and Splitter as targets.
        """
        if self.is_open and self.source and self.source.current_volume >= self.rate:
            self.source.current_volume -= self.rate

            if isinstance(self.target, Tank):
                self.target.transfer(self.rate)
            elif isinstance(self.target, Splitter):
                self.target.distribute(self.rate)  # Call the distribute method for Splitter
            else:
                print(f"[Pump {self.id}] Warning: Unsupported target type {type(self.target)}")
        elif self.is_open and self.source and self.source.current_volume > 0:
            # Transfer remaining volume if less than rate
            transfer_amount = self.source.current_volume
            self.source.current_volume = 0

            if isinstance(self.target, Tank):
                self.target.transfer(transfer_amount)
            elif isinstance(self.target, Splitter):
                self.target.distribute(transfer_amount)
            else:
                print(f"[Pump {self.id}] Warning: Unsupported target type {type(self.target)}")

    def publish(self):
        """
        Publishes current rate and state to MQTT topics.
        """
        self.mqtt.publish(f"pump/{self.id}/rate", self.rate)
        self.mqtt.publish(f"pump/{self.id}/state", "open" if self.is_open else "closed")
        print(f"[Pump {self.id}] Published rate: {self.rate}, state: {'open' if self.is_open else 'closed'}")

    def get_rate(self):
        """Returns the current flow rate."""
        return self.rate

    def set_rate(self, new_rate):
        """Sets a new flow rate."""
        self.rate = new_rate

    def get_state(self):
        """Returns the current state of the pump ('open' or 'closed')."""
        return "open" if self.is_open else "closed"

    def set_state(self, state: str):
        """Sets the state of the pump ('open' or 'closed')."""
        self.is_open = state.lower() == "open"
