import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import warnings

# Suppress DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Create client with MQTT v5
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="mqtt_v5_test", protocol=mqtt.MQTTv5)

# Define callbacks
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with reason code: {reason_code}")
    client.publish("test/topic", "Hello MQTT v5!")

def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"Disconnected with reason code: {reason_code}")

# Assign callbacks
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Set MQTT v5 CONNECT properties
props = Properties(PacketTypes.CONNECT)
props.SessionExpiryInterval = 60  # Optional

# Connect and start loop
client.connect("localhost", 1883, keepalive=60, clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY, properties=props)
client.loop_start()

# Let it run for a bit
time.sleep(2)

client.disconnect()
client.loop_stop()
