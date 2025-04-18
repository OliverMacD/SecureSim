"""
MQTT Interface for Process Simulation

This module provides a threaded MQTT client interface built on top of `gmqtt`.
It supports asynchronous publishing, topic subscription, and simulated testing.

Classes:
    MQTTInterface - Manages connection to a broker, topic subscriptions, and message handling.
"""

import asyncio
import threading
import time
import os
from gmqtt import Client as MQTTClient


class MQTTInterface:
    """
    A threaded MQTT client interface for real-time message exchange between process components.

    Features:
      - Asynchronous background MQTT loop using `gmqtt`
      - Auto-reconnection handling
      - Topic-based callbacks
      - Support for simulated message injection (for testing)
    """

    def __init__(self, broker="127.0.0.1", port=1883, client_id="process_sim_client", token=None):
        """
        Initializes the MQTT client and starts the background event loop.

        Args:
            broker (str): IP address of the MQTT broker.
            port (int): Port number for MQTT (default: 1883).
            client_id (str): Unique client identifier.
            token (str): Optional token for authentication.
        """
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

        # Launch background thread to run the client loop
        self._thread = threading.Thread(target=self._start_loop, daemon=True)
        self._thread.start()

    def _start_loop(self):
        """Starts the asyncio loop in the thread context."""
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect_and_listen())

    async def _connect_and_listen(self):
        """
        Connects to the broker and keeps the event loop alive.
        Reconnects automatically if connection drops.
        """
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
        """
        Publishes data to a specific MQTT topic.

        Args:
            topic (str): Topic to publish to.
            data (str or float): Message payload.
            qos (int): Quality of Service level (default: 0).
        """
        if self._connected:
            self._loop.call_soon_threadsafe(self._client.publish, topic, str(data), qos)
        else:
            print(f"[MQTT-ERR] Not connected. Failed to publish to {topic}")

    def subscribe(self, topic, callback):
        """
        Subscribes to a topic and registers a callback to handle messages.

        Args:
            topic (str): Topic to subscribe to.
            callback (function): Function to handle incoming messages.
        """
        self._subscribers[topic] = callback
        if self._connected:
            self._loop.call_soon_threadsafe(self._client.subscribe, topic)
        print(f"[MQTT-SUB] Subscribed to: {topic}")

    def _on_connect(self, client, flags, rc, properties):
        """Handler triggered when the client connects to the broker."""
        print(f"[MQTT] Connected with flags: {flags}, rc: {rc}")
        for topic in self._subscribers:
            self._loop.call_soon_threadsafe(client.subscribe, topic)

    def _on_disconnect(self, client, packet, exc=None):
        """Handler triggered when the client disconnects from the broker."""
        self._connected = False
        print(f"[MQTT] Disconnected")

    def _on_subscribe(self, client, mid, qos, properties):
        """Handler triggered after a successful subscription."""
        print(f"[MQTT] Subscribed successfully")

    def _on_message(self, client, topic, payload, qos, properties):
        """
        Dispatches received messages to the appropriate subscriber callback.

        Args:
            topic (str): Topic on which message was received.
            payload (bytes or str): Message content.
        """
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
        """
        Sends a simulated message to a topic handler without a broker.
        Useful for unit testing.

        Args:
            topic (str): Target topic.
            payload (str): Simulated payload.
        """
        print(f"[MQTT-SIM] {topic}: {payload}")
        if topic in self._subscribers:
            self._subscribers[topic](payload)
        else:
            print(f"[MQTT-SIM-WARN] No subscriber for topic: {topic}")
