# process_sim

A modular, MQTT-enabled simulation framework for modeling and visualizing fluid-based process systems such as water treatment, manufacturing, and other SCADA-style environments.

---

## 📦 Package Structure

```
process_sim/
│
├── base.py                  # Base class for all process components
├── tank.py                  # Tank implementation with MQTT control
├── pump.py                  # Pump implementation with MQTT control
├── splitter.py              # Splitter for distributing flow
├── line.py                  # Connects nodes and moves flow
│
├── layout_parser.py         # Parses a layout JSON into a process graph
├── simulation_runner.py     # Runs the simulation on a background thread
├── graph_visualizer.py      # Graph rendering utilities
│
├── interfaces/
│   └── mqtt_interface.py    # MQTT publish/subscribe abstraction
│
└── __init__.py              # Unified import interface
```

---

## 🔁 Quick Example

```python
from process_sim import (
    init_mqtt, load_layout, SimulationThread, render_process_graph
)

# Initialize MQTT
init_mqtt(broker="127.0.0.1", port=1883)

# Load graph layout
graph = load_layout("example_layout.json")

# Render static graph layout
render_process_graph(graph)

# Start simulation thread
sim = SimulationThread(graph, interval=1.0, debug=True)
sim.start()
```

---

## 🧱 Core Components

### `Tank`
- Stores fluid and accepts incoming flow.
- Controlled via MQTT:
  - `get/set` max capacity
  - `get` current capacity

### `Pump`
- Transfers fluid from a source to a target.
- Controlled via MQTT:
  - `get/set` rate
  - `get/set` open/closed state

### `Splitter`
- Evenly splits incoming flow across multiple outputs.

### `Line`
- Transfers flow between components.
- Publishes current buffer size to MQTT.

---

## 🧠 Simulation Loop

Use the `SimulationThread` to:
- Call `update()` on all nodes/lines to perform logic.
- Call `publish()` to send system state to MQTT.

Optional `debug=True` displays a real-time network graph.

---

## 🗺️ Layout Format

Input JSON layout must define:
- `nodes`: ID, type (`Tank`, `Pump`, `Splitter`), name, position
- `edges`: ID, name, source ID, target ID

A full JSON layout example & explanation can be found in the [JSON](./JSON.md) document

---

## 📡 MQTT Interface

- Topics follow the format:  
  `get/<type>/<id>/<attribute>`  
  `set/<type>/<id>/<attribute>`  
  `state/<type>/<id>/<attribute>`  

- Example:
  ```bash
  mosquitto_pub -t set/pump/P1/state -m "closed"
  mosquitto_pub -t set/tank/T1/max_capacity -m "1000"
  ```

- Simulate messages in code:
  ```python
  from process_sim import simulate_mqtt_message
  simulate_mqtt_message("set/pump/P1/state", "open")
  ```

---

## 📊 Visualization

### Static Graph
```python
render_process_graph(graph)
```

### Live Graph
Included in `SimulationThread(debug=True)` or standalone:
```python
render_live_graph(graph)
```