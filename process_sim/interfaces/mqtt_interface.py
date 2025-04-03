# process_sim/interfaces/mqtt_interface.py

import paho.mqtt.client as mqtt
import threading

_broker = "localhost"
_port = 1883
_client = None
_connected = False
_subscribers = {}

def publish_mqtt(topic, data):
    if _connected:
        _client.publish(topic, str(data))
        print(f"[MQTT-PUB] {topic}: {data}")
    else:
        print(f"[MQTT-ERR] Not connected. Failed to publish to {topic}")

def subscribe_mqtt(topic, callback):
    _subscribers[topic] = callback
    if _connected:
        _client.subscribe(topic)
    print(f"[MQTT-SUB] Subscribed to: {topic}")

def on_connect(client, userdata, flags, rc):
    global _connected
    _connected = True
    print("[MQTT] Connected to broker.")
    # Resubscribe to all topics after (re)connect
    for topic in _subscribers:
        client.subscribe(topic)
        print(f"[MQTT] Subscribed to: {topic}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[MQTT-RX] {topic}: {payload}")
    if topic in _subscribers:
        try:
            _subscribers[topic](payload)
        except Exception as e:
            print(f"[MQTT-ERR] Error in subscriber callback: {e}")
    else:
        print(f"[MQTT-WARN] No subscriber for topic: {topic}")

def init_mqtt(broker="localhost", port=1883):
    global _client, _broker, _port

    _broker = broker
    _port = port
    _client = mqtt.Client()

    _client.on_connect = on_connect
    _client.on_message = on_message

    try:
        _client.connect(_broker, _port, 60)
        thread = threading.Thread(target=_client.loop_forever, daemon=True)
        thread.start()
        print(f"[MQTT] Client started on {broker}:{port}")
    except Exception as e:
        print(f"[MQTT-ERR] Failed to connect to MQTT broker: {e}")

def simulate_mqtt_message(topic, payload):
    """Optional helper for unit testing without an actual broker"""
    print(f"[MQTT-SIM] {topic}: {payload}")
    if topic in _subscribers:
        _subscribers[topic](payload)
    else:
        print(f"[MQTT-SIM-WARN] No subscriber for topic: {topic}")
