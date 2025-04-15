"""
Line Component

Represents a directed connection between two process components. Temporarily stores and transfers
flow from a source to a target node in the simulation.

Classes:
    Line - Holds flow between components and pushes it downstream on each update cycle.
"""

from process_sim.base import ProcessComponent

class Line(ProcessComponent):
    """
    A process connection that carries flow between a source and a target.
    The line acts as a buffer until its `update` method is called.
    """

    def __init__(self, id, name, source=None, target=None):
        """
        Args:
            id (str): Unique identifier for the line.
            name (str): Human-readable name.
            source (ProcessComponent, optional): The component sending flow.
            target (ProcessComponent, optional): The component receiving flow.
        """
        super().__init__(id, name)
        self.source = source
        self.target = target
        self.buffer = 0.0  # Holds fluid until transferred

    def transfer(self, amount):
        """
        Adds an amount of flow to the buffer.

        Args:
            amount (float): Amount of fluid to transfer.
        """
        self.buffer += amount

    def update(self):
        """
        Sends the buffered flow to the target component and clears the buffer.
        """
        if self.target and self.buffer > 0:
            self.target.receive(self.buffer)
            self.buffer = 0.0

    def publish(self):
        """
        No active state to publish. Exists for interface compatibility.
        """
        pass
