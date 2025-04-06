# 📄 JSON Layout Specification for `process_sim`

This document defines the JSON format used to describe a complete fluid process system in the `process_sim` package. It includes:

- Nodes (components)
- Edges (connections)
- PLC configurations
- SCADA configurations

---

## 🧠 Overview

The `layout_parser.load_layout()` function in `process_sim` reads this JSON structure to build a complete simulation graph. It supports visual simulation, MQTT-based telemetry, and integration with PLC/SCADA systems.

---

## 🧱 Top-Level Structure

```json
{
  "nodes": [...],
  "edges": [...],
  "plcs": [...],
  "scada": {...}
}
```

Each key is explained in detail below.

---

## 🔵 Nodes

Defines all components in the system. Supported types:
- `Tank`
- `Pump`
- `Splitter`

### 🧪 Example

```json
{
  "id": "tank1",
  "type": "Tank",
  "name": "Main Tank",
  "max_capacity": 1000,
  "initial_capacity": 900,
  "position": [0, 0]
}
```

### 🔍 Tank Attributes

| Field             | Type     | Required | Description |
|------------------|----------|----------|-------------|
| `id`             | string   | ✅       | Unique ID of the tank |
| `type`           | `"Tank"` | ✅       | Must be `"Tank"` |
| `name`           | string   | ✅       | Human-readable name |
| `max_capacity`   | number   | ✅       | Maximum storage |
| `initial_capacity` | number | ❌       | Starting fluid volume (default: 0) |
| `position`       | [x, y]   | ❌       | Coordinates for visualization |

---

### 🔧 Pump Attributes

```json
{
  "id": "pump1",
  "type": "Pump",
  "name": "Pump A",
  "flow_rate": 50,
  "source": "tank1",
  "is_open": true,
  "position": [2, 0]
}
```

| Field       | Type     | Required | Description |
|------------|----------|----------|-------------|
| `type`     | `"Pump"` | ✅       | Must be `"Pump"` |
| `flow_rate`| number   | ✅       | Rate of fluid transfer |
| `source`   | string   | ✅       | ID of source tank |
| `is_open`  | bool     | ❌       | Initial state (default: `true`) |

---

### 🔀 Splitter Attributes

```json
{
  "id": "splitter1",
  "type": "Splitter",
  "name": "Splitter A",
  "position": [4, 0]
}
```

| Field   | Type     | Required | Description |
|--------|----------|----------|-------------|
| `type` | `"Splitter"` | ✅ | Distributes flow evenly to multiple outputs |

---

## ➰ Edges

Define directional flow lines between components.

### 🔗 Example

```json
{
  "id": "line1",
  "name": "Line 1",
  "source": "pump1",
  "target": "splitter1"
}
```

| Field     | Type   | Required | Description |
|----------|--------|----------|-------------|
| `id`     | string | ✅       | Unique ID of the line |
| `name`   | string | ✅       | Name for label |
| `source` | string | ✅       | ID of source node |
| `target` | string | ✅       | ID of target node |

---

## 🧩 PLCs

Defines Modbus PLCs managing a subset of devices.

### 🧾 Example

```json
{
  "id": "plc1",
  "ip": "127.0.0.1",
  "port": 5100,
  "devices": [
    {
      "id": "tank1",
      "type": "Tank",
      "mqtt_topic": "device/tank1/data",
      "plc_input_register": 0
    }
  ]
}
```

| Field               | Type     | Description |
|--------------------|----------|-------------|
| `id`               | string   | Unique PLC ID |
| `ip`               | string   | PLC host IP |
| `port`             | int      | Port number for Modbus |
| `devices`          | list     | Devices handled by this PLC |

Each device maps an MQTT stream to a register.

---

## 🖥️ SCADA Configuration

Top-level SCADA controller register map.

### ⚙️ Example

```json
"scada": {
  "ip": "127.0.0.1",
  "port": 5200,
  "register_map": {
    "tank1": 0,
    "tank2": 1,
    "tank3": 2,
    "pump1": 10
  }
}
```

| Field         | Type     | Description |
|--------------|----------|-------------|
| `ip`         | string   | Host IP of SCADA Modbus listener |
| `port`       | int      | Modbus port |
| `register_map` | dict   | Maps component ID to register |

---

## 📌 Layout Loading in Python

```python
from process_sim import load_layout

graph = load_layout("path/to/layout.json")
```

The resulting `ProcessGraph` object contains:
- `graph.nodes`: all Tank, Pump, Splitter objects
- `graph.lines`: all Line objects

---

## ✅ Validation Tips

- All `id`s must be unique.
- Every `source` and `target` in `edges` must refer to an existing node.
- Pumps must declare `source`, while lines define the `target`.

---

## 📬 Need Help?

If you're unsure whether your layout is valid, try loading it in Python and catching exceptions:

```python
try:
    graph = load_layout("layout.json")
except Exception as e:
    print("Layout error:", e)
```
