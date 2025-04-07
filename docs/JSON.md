# 📄 JSON Layout Specification for `process_sim`

This document defines the JSON format used to describe a complete fluid process system in the `process_sim` package. It includes:

- Nodes (components)
- Edges (connections)
- PLC configurations
- SCADA configurations

---

## 🧠 Overview

The `layout_parser.load_layout()` function reads this JSON structure to build a simulation graph. The format supports:

- Visual system modeling
- MQTT telemetry and control
- Modbus-based PLC/SCADA simulation
- Security testing via false data injection, DoS, and replay

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

Each section is described below.

---

## 🔵 Nodes

Defines all fluid-handling components.

### Supported Types

- `Tank`
- `Pump`
- `Splitter`

### 🧪 Tank Example

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

| Field              | Type     | Required | Description |
|-------------------|----------|----------|-------------|
| `id`              | string   | ✅       | Unique identifier |
| `type`            | `"Tank"` | ✅       | Component type |
| `name`            | string   | ✅       | Label for UI |
| `max_capacity`    | number   | ✅       | Full volume |
| `initial_capacity`| number   | ❌       | Start value (default: 0) |
| `position`        | [x, y]   | ❌       | UI layout only |

---

### ⚙️ Pump Example

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
| `type`     | `"Pump"` | ✅       | Component type |
| `source`   | string   | ✅       | ID of input tank |
| `flow_rate`| number   | ✅       | Units per update |
| `is_open`  | boolean  | ❌       | Initial state |
| `position` | [x, y]   | ❌       | UI layout only |

---

### 🔀 Splitter Example

```json
{
  "id": "splitter1",
  "type": "Splitter",
  "name": "Splitter A",
  "position": [4, 0]
}
```

| Field   | Type       | Required | Description |
|--------|------------|----------|-------------|
| `type` | `"Splitter"`| ✅      | Evenly divides flow |
| `position` | [x, y]   | ❌      | Visual layout only |

---

## ➰ Edges

Define connections between nodes using `source` and `target` references.

### 🔗 Edge Example

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
| `id`     | string | ✅       | Unique identifier |
| `name`   | string | ✅       | Label for diagram |
| `source` | string | ✅       | Upstream node ID |
| `target` | string | ✅       | Downstream node ID |

---

## 🧩 PLCs

Each PLC handles a subset of the system and supports automated logic.

### Example

```json
{
  "id": "plc1",
  "ip": "127.0.0.1",
  "port": 5100,
  "devices": [
    {
      "id": "tank1",
      "type": "Tank",
      "mqtt_topic": "tank/tank1/volume",
      "plc_input_register": 0
    }
  ],
  "actions": [
    {
      "name": "Close if Tank1 Empty",
      "trigger": { "register": 0, "condition": "==", "value": 0 },
      "effect": { "target": "pump1", "action": "close" }
    }
  ]
}
```

### 🔍 PLC Device Fields

| Field              | Type     | Description |
|-------------------|----------|-------------|
| `id`              | string   | Component ID |
| `type`            | string   | `"Tank"`, `"Pump"`, etc |
| `mqtt_topic`      | string   | MQTT topic for state |
| `plc_input_register` | int  | Register number |

### ⚡ PLC Action Fields

| Field      | Type | Description |
|-----------|------|-------------|
| `trigger` | dict | Condition on a register |
| `effect`  | dict | What to do (e.g. open/close a pump) |

> PLC actions are evaluated every simulation tick.

---

## 🖥️ SCADA

Top-level controller that can:
- Mirror system state
- Respond to emergency registers
- Interface with HMI or attacks

### SCADA Example

```json
"scada": {
  "ip": "127.0.0.1",
  "port": 5200,
  "register_map": {
    "tank1": 0,
    "pump1": 10,
    "emergency_stop": 99
  },
  "actions": [
    {
      "name": "Emergency Shutdown",
      "trigger": { "register": 99, "condition": "==", "value": 1 },
      "effect": { "target": ["pump1"], "action": "close" }
    }
  ]
}
```

| Field         | Type  | Description |
|---------------|-------|-------------|
| `ip`          | string| Modbus IP for HMI |
| `port`        | int   | Modbus port |
| `register_map`| dict  | Maps device ID → register |
| `actions`     | list  | Emergency rules (like PLCs) |

---

## 🔂 MQTT Integration

Each device includes a `mqtt_topic` for publishing values and listening to set commands:

| Type | Topic Format | Description |
|------|--------------|-------------|
| Tank | `tank/{id}/volume` | Volume state |
| Pump | `pump/{id}/state`, `pump/{id}/rate` | State or rate |
| Set  | `set/tank/{id}/max_capacity` | Writable config |

---

## 📌 Using in Code

```python
from process_sim.layout_parser import load_layout
graph = load_layout("path/to/layout.json")
```

You can access:
- `graph.nodes`: all components
- `graph.lines`: all connections
- `graph.plc_configs`: full PLC list
- `graph.scada_config`: top-level SCADA dictionary

---

## ✅ Best Practices

- Keep `id` fields globally unique.
- Use MQTT for real-time controls; use Modbus for HMI and attack testing.
- Prefer numeric register indexes below 100.
- Use `actions` to encode safety and logic rules.

---
