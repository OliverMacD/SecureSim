# broker_test.py

import asyncio
import time
from gmqtt import Client as MQTTClient

connected = asyncio.Event()
received_messages = []

def on_connect(client, flags, rc, properties):
    print(f"[TEST] Connected with code: {rc}")
    client.subscribe("test/topic")

def on_disconnect(client, packet, exc=None):
    print(f"[TEST] Disconnected")

def on_message(client, topic, payload, qos, properties):
    print(f"[TEST] Received message on {topic}: {payload.decode()}")
    received_messages.append(payload.decode())

async def main():
    client = MQTTClient("mqtt_v5_test")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    await client.connect("127.0.0.1", 1883)

    try:
        await asyncio.sleep(1)
        client.publish("test/topic", "222")
        await asyncio.sleep(2)
        client.publish("test/topic", "333")
        await asyncio.sleep(2)
    finally:
        await client.disconnect()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[TEST] Keyboard interrupt received. Exiting cleanly.")
