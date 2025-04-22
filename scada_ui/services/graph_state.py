from scada_ui.services.mqtt_interface import MQTTInterface

mqtt = MQTTInterface()
latest_values = {}

def handle_mqtt_message(topic, message):
    if message is not None:
        latest_values[topic] = message  # Cache latest non-null message

# Subscribe to all known process topics at startup
topics_to_subscribe = [
    "pump/pump1/state", "pump/pump2/state", "pump/pump3/state",
    "pump/pump4/state", "pump/pump5/state", "pump/pump6/state",
    "tank/tank1/volume", "tank/tank2/volume", "tank/tank3/volume",
    "tank/tank4/volume", "tank/tank5/volume", "tank/tank6/volume"
]

for topic in topics_to_subscribe:
    mqtt.subscribe(topic, lambda msg, t=topic: handle_mqtt_message(t, msg))

def get_modbus_state(topic):
    # Return cached value or "unknown" if not yet received
    return latest_values.get(topic, "unknown")