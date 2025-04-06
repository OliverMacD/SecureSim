# server/mqtt_server.py
import asyncio
from mqttools.broker import Broker

async def mqttServer():
    print("[MQTT] Starting MQTT broker on 127.0.0.1:1883...")
    broker = Broker(('127.0.0.1', 1883))

    await broker.serve_forever()

if __name__ == '__main__':
    asyncio.run(mqttServer())