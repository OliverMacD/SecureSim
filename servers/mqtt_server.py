# server/mqtt_server.py

import asyncio
import logging
from mqttools.broker import Broker

# Optional: Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    print("[MQTT] Starting MQTT broker on localhost:1883...")
    broker = Broker(('localhost', 1883))

    await broker.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
