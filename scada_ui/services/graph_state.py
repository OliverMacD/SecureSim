from scada_ui.services.mqtt_interface import MQTTInterface

# Assuming MQTTInterface is used for communication with Modbus
mqtt = MQTTInterface()

def get_modbus_state(topic):
    """
    Fetches the state for a given topic via MQTT (Modbus).
    This function should handle subscribing to the topic and returning the state.
    """
    # Placeholder: Replace with actual Modbus MQTT interaction
    # Example: Use the MQTTInterface to get the state for a particular topic
    result = None

    def handle_message(msg):
        nonlocal result
        result = msg  # Capture the message in the result variable
    
    mqtt.subscribe(topic, handle_message)  # Subscribe to the topic
    
    # Give some time for the message to arrive before returning the result
    import time
    time.sleep(1)  # Adjust this sleep time based on your system's response time
    
    if result is None:
        print(f"[ERROR] No data received for topic {topic}")
    
    return result
