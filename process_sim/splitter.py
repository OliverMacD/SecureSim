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
        self.outputs = []  # List of output lines connected to the splitter

    def add_output(self, line):
        """
        Connects an outgoing line to the splitter.

        Args:
            line (Line): A process line to which flow will be routed.
        """
        self.outputs.append(line)

    def distribute(self, amount):
        """
        Distributes a volume of fluid equally to all connected outputs.

        Args:
            amount (float): The volume of fluid to distribute.
        """
        if not self.outputs:
            print(f"[Splitter {self.id}] Warning: No outputs to distribute to.")
            return

        # Calculate the amount to send to each output
        split_amount = amount / len(self.outputs)
        for line in self.outputs:
            if line.target:
                line.target.transfer(split_amount)
                print(f"[Splitter {self.id}] Transferred {split_amount} units to {line.target.id}")

    def update(self):
        """
        Updates the splitter's state. No internal state to update, but method exists
        for interface consistency.
        """
        pass

    def publish(self):
        """
        Publishes the splitter's state. No active state to publish, but method exists
        for interface consistency.
        """
        pass