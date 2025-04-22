import time

class RateLimiter:
    """
    Implements a rate-limiting mechanism to prevent DoS attacks.
    """
    def __init__(self, max_messages_per_second=10):
        """
        Args:
            max_messages_per_second (int): Maximum allowed messages per second.
        """
        self.max_messages_per_second = max_messages_per_second
        self.message_timestamps = []

    def allow_message(self):
        """
        Checks if a new message can be processed based on the rate limit.

        Returns:
            bool: True if the message is allowed, False otherwise.
        """
        current_time = time.time()
        self.message_timestamps = [
            ts for ts in self.message_timestamps if current_time - ts < 1
        ]

        if len(self.message_timestamps) < self.max_messages_per_second:
            self.message_timestamps.append(current_time)
            return True
        return False