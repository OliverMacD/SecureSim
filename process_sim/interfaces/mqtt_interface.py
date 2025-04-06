# process_sim/interfaces/mqtt_interface.py

import asyncio
import threading
import time
import os

from gmqtt import Client as MQTTClient


class MQTTInterface:
    def __init__(self, broker="127.0.0.1", port=1883, client_id="process_sim_client", token=None):
        self._broker = broker
        self._port = port
        self._client_id = client_id
        self._token = token
        self._connected = False
        self._client = MQTTClient(self._client_id)
        self._subscribers = {}
        self._loop = asyncio.new_event_loop()

        # Setup handlers
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message
        self._client.on_subscribe = self._on_subscribe

        if self._token:
            self._client.set_auth_credentials(self._token, None)

        # Run the MQTT loop in a background thread
        self._thread = threading.Thread(target=self._start_loop, daemon=True)
        self._thread.start()

    def _start_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect_and_listen())

    async def _connect_and_listen(self):
        try:
            await self._client.connect(self._broker, self._port)
            self._connected = True
            print(f"[MQTT] Connected to {self._broker}:{self._port} as {self._client_id}")
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            print(f"[MQTT-ERR] Failed to connect or lost connection: {e}")
            self._connected = False

    def publish(self, topic, data, qos=0):
        if self._connected:
            self._loop.call_soon_threadsafe(self._client.publish, topic, str(data), qos)
        else:
            print(f"[MQTT-ERR] Not connected. Failed to publish to {topic}")

    def subscribe(self, topic, callback):
        self._subscribers[topic] = callback
        if self._connected:
            self._loop.call_soon_threadsafe(self._client.subscribe, topic)
        print(f"[MQTT-SUB] Subscribed to: {topic}")

    def _on_connect(self, client, flags, rc, properties):
        print(f"[MQTT] Connected with flags: {flags}, rc: {rc}")
        for topic in self._subscribers:
            self._loop.call_soon_threadsafe(client.subscribe, topic)

    def _on_disconnect(self, client, packet, exc=None):
        self._connected = False
        print(f"[MQTT] Disconnected")

    def _on_subscribe(self, client, mid, qos, properties):
        print(f"[MQTT] Subscribed successfully")

    def _on_message(self, client, topic, payload, qos, properties):
        message = payload.decode() if isinstance(payload, bytes) else payload
        print(f"[MQTT-RX] {topic}: {message}")
        if topic in self._subscribers:
            try:
                self._subscribers[topic](message)
            except Exception as e:
                print(f"[MQTT-ERR] Error in subscriber callback: {e}")
        else:
            print(f"[MQTT-WARN] No subscriber for topic: {topic}")

    def simulate_message(self, topic, payload):
        """Optional helper for unit testing without an actual broker"""
        print(f"[MQTT-SIM] {topic}: {payload}")
        if topic in self._subscribers:
            self._subscribers[topic](payload)
        else:
            print(f"[MQTT-SIM-WARN] No subscriber for topic: {topic}")
