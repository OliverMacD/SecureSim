"""
MQTT Broker Starter

This module starts a local MQTT broker using the mqttools library.
It is used for communication between simulation components and control logic.

Usage:
    Run this script directly to start the broker:
    $ python mqtt_server.py

Functions:
    mqttServer - Asynchronously starts the MQTT broker.
"""

import asyncio
from mqttools.broker import Broker

async def mqttServer():
    """
    Starts an MQTT broker on localhost (127.0.0.1) at port 1883.
    This broker allows publish/subscribe communication between process components.
    """
    print("[MQTT] Starting MQTT broker on 127.0.0.1:1883...")
    broker = Broker(('127.0.0.1', 1883))
    await broker.serve_forever()

if __name__ == '__main__':
    asyncio.run(mqttServer())
