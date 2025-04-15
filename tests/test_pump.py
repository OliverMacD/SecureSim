import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from process_sim.tank import Tank
from process_sim.pump import Pump
from process_sim.interfaces.mqtt_interface import MQTTInterface

class MockMQTTInterface(MQTTInterface):
    def __init__(self):
        self.messages = {}

    def publish(self, topic, message):
        self.messages[topic] = message
        print(f"MQTT Publish -> Topic: {topic}, Message: {message}")

    def subscribe(self, topic, callback):
        print(f"MQTT Subscribe -> Topic: {topic}")

# Setup test components
def test_pump_and_tank():
    mqtt = MockMQTTInterface()

    # Create tanks
    source_tank = Tank(id="tank1", name="Source Tank", max_capacity=1000, mqtt_interface=mqtt)
    target_tank = Tank(id="tank2", name="Target Tank", max_capacity=500, mqtt_interface=mqtt)

    # Fill the source tank
    source_tank.current_volume = 800

    # Create a pump
    pump = Pump(id="pump1", name="Test Pump", rate=200, mqtt_interface=mqtt, is_open=True)
    pump.set_connection(source_tank, target_tank)

    # Simulate pump operation
    print("\n--- Pump Test Start ---")
    for _ in range(5):  # Simulate 5 update cycles
        pump.update()
        source_tank.publish()
        target_tank.publish()
        pump.publish()
    print("--- Pump Test End ---")

# Run the test
if __name__ == "__main__":
    test_pump_and_tank()