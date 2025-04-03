# server/mqtt_server.py

import asyncio
from hbmqtt.broker import Broker

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': 'localhost:1883'
        }
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True
    }
}

broker = Broker(config)

async def run_broker():
    print("[MQTT] Starting real MQTT broker on localhost:1883...")
    await broker.start()

if __name__ == "__main__":
    asyncio.run(run_broker())
