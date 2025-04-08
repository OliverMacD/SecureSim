JSON Structure
==============

The `Process_sim.json` file defines the entire simulated environment, including nodes (tanks, pumps, etc.), connections (lines), and logic (PLCs, SCADA).

Top-Level Structure
-------------------

The layout file must follow this format:

.. code-block:: javascript

    {
      "nodes": [...],
      "edges": [...],
      "plcs": [...],
      "scada": {...}
    }

Each key is explained below.

Nodes
-----

Nodes represent components in the process system.

Supported types:
- ``Tank``
- ``Pump``
- ``Splitter``

.. code-block:: json

    {
      "id": "tank1",
      "type": "Tank",
      "name": "Main Tank",
      "max_capacity": 1000,
      "initial_capacity": 900,
      "position": [0, 0]
    }

Node Fields:

- ``id``: Unique identifier (required)
- ``type``: Component type (`Tank`, `Pump`, `Splitter`)
- ``name``: Display name for UI
- ``max_capacity``: Max volume (for tanks)
- ``flow_rate``: Transfer rate (for pumps)
- ``source``: Source node (for pumps)
- ``is_open``: Whether pump is initially open
- ``position``: Optional `[x, y]` position for UI

Edges
-----

Edges define connections between nodes using a Line object.

.. code-block:: json

    {
      "id": "line1",
      "name": "Waste Line",
      "source": "pump1",
      "target": "tank2"
    }

Fields:

- ``id``: Unique line ID
- ``source``: Upstream node ID
- ``target``: Downstream node ID

PLCs
----

Each PLC defines:
- Which devices it monitors (via Modbus registers)
- What logic to apply (rules/actions)

.. code-block:: json

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
          "name": "Close if empty",
          "trigger": { "register": 0, "condition": "==", "value": 0 },
          "effect": { "target": "pump1", "action": "close" }
        }
      ]
    }

Action Fields:
- ``trigger``: Register-based condition (e.g., tank1.volume == 0)
- ``effect``: What to do (e.g., close a pump)

SCADA
-----

SCADA logic mirrors PLC logic, but centrally. It can also include override/emergency rules.

.. code-block:: json

    {
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

Design Tips
-----------

- Keep register numbers unique per device
- Use short IDs for compact MQTT topics
- Position values are optional and only for UI

Usage in Code
-------------

Load a layout with:

.. code-block:: python

    from process_sim.layout_parser import load_layout
    graph = load_layout("Process_sim.json")