"""
Splitter Component

Represents a passive component in the process simulation that evenly distributes
incoming flow to multiple outgoing lines.

Classes:
    Splitter - Splits received volume equally across its outputs.
"""

from process_sim.base import ProcessComponent

class Splitter(ProcessComponent):
    """
    A passive process component that splits input flow evenly between all connected outputs.
    """

    def __init__(self, id, name):
        """
        Args:
            id (str): Unique identifier for the splitter.
            name (str): Human-readable name.
        """
        super().__init__(id, name)
        self.outputs = []

    def add_output(self, line):
        """
        Connects an outgoing line to the splitter.

        Args:
            line (Line): A process line to which flow will be routed.
        """
        self.outputs.append(line)

    def receive(self, amount):
        """
        Receives a volume of fluid and distributes it equally to all outputs.

        Args:
            amount (float): The volume of fluid to distribute.
        """
        if not self.outputs:
            return
        split_amount = amount / len(self.outputs)
        for out in self.outputs:
            out.transfer(split_amount)

    def update(self):
        """
        No internal state to update. Method exists for interface consistency.
        """
        pass

    def publish(self):
        """
        No active state to publish. Method exists for interface consistency.
        """
        pass
