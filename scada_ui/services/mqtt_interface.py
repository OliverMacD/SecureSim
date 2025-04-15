import asyncio
import threading
from gmqtt import Client as MQTTClient

class MQTTInterface:
    def __init__(self, broker="127.0.0.1", port=1883, client_id="process_sim_client"):
        self._broker = broker
        self._port = port
        self._client_id = client_id
        self._client = MQTTClient(self._client_id)
        self._connected = False
        self._loop = asyncio.new_event_loop()
        self._subscribers = {}

        # Setup handlers
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        # Start background thread
        self._thread = threading.Thread(target=self._start_loop, daemon=True)
        self._thread.start()

    def _start_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect_and_listen())

    async def _connect_and_listen(self):
        try:
            await self._client.connect(self._broker, self._port)
            self._connected = True
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            print(f"MQTT Error: {e}")
            self._connected = False

    def subscribe(self, topic, callback):
        if self._connected:
            self._loop.call_soon_threadsafe(self._client.subscribe, topic)
            self._subscribers[topic] = callback

    def publish(self, topic, data):
        if self._connected:
            self._loop.call_soon_threadsafe(self._client.publish, topic, str(data))

    def _on_connect(self, client, flags, rc, properties):
        for topic in self._subscribers:
            self._loop.call_soon_threadsafe(client.subscribe, topic)

    def _on_message(self, client, topic, payload, qos, properties):
        """
        Dispatches received messages to the appropriate subscriber callback.
        """
        message = payload.decode() if isinstance(payload, bytes) else payload
        print(f"[MQTT-RX] {topic}: {message}")  # Debugging line to check incoming message
        if topic in self._subscribers:
            try:
                self._subscribers[topic](message)
            except Exception as e:
                print(f"[MQTT-ERR] Error in subscriber callback: {e}")
        else:
            print(f"[MQTT-WARN] No subscriber for topic: {topic}")

