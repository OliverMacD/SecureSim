"""
Base Process Component

This module defines the abstract base class `ProcessComponent`, which all simulation
components inherit from. It ensures that each component implements the required `update`
and `publish` methods for simulation behavior and communication.

Classes:
    ProcessComponent - Abstract interface for all process simulation components.
"""

class ProcessComponent:
    """
    Abstract base class for all process simulation components.

    All components must implement:
      - update(): to handle internal logic and state progression.
      - publish(): to share current state via external interfaces (e.g., MQTT).
    """

    def __init__(self, id, name):
        """
        Args:
            id (str): Unique identifier of the component.
            name (str): Human-readable name of the component.
        """
        self.id = id
        self.name = name

    def update(self):
        """
        Perform any internal state updates for the component.
        Must be overridden by subclass.
        """
        raise NotImplementedError("Must implement update method.")
    
    def publish(self):
        """
        Publish component state to the outside world (e.g., via MQTT).
        Must be overridden by subclass.
        """
        raise NotImplementedError("Must implement publish method.")
