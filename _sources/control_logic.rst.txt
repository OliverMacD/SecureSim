Control Logic
=============

SecureSim includes programmable control logic via:

- **PLCs**: Local controllers that act on a subset of devices
- **SCADA**: Central control system for monitoring and emergency responses
- **Action Engine**: Shared rule evaluation system

PLC Controllers
---------------

PLCs define control logic based on:

- Inputs from connected devices (via MQTT or Modbus)
- Actions that operate on those devices (e.g., open/close a pump)

Each PLC is described in the JSON layout and launched using:

- `plc.py`: Base logic wrapper
- `plc_modbus.py`: Adds Modbus server and register interaction

PLCs run a `ModbusServerWrapper` and expose control registers per device.

Example behavior:

.. code-block:: json

    {
      "trigger": { "register": 0, "condition": ">", "value": 500 },
      "effect": { "target": "pump1", "action": "open" }
    }

SCADA System
------------

The SCADA unit is a centralized controller that:

- Monitors all devices
- Publishes data via Modbus
- Supports global overrides

SCADA uses:

- `scada.py`: Core logic runner
- `scada_modbus.py`: Registers and control

Example:

.. code-block:: json

    {
      "trigger": { "register": 99, "condition": "==", "value": 1 },
      "effect": { "target": ["pump1", "pump2"], "action": "close" }
    }

Action Engine
-------------

All logic is executed via the `ActionEngine` class:

1. It reads the trigger condition
2. Resolves the register to a device
3. Gets the current state/volume
4. Compares it to the condition
5. Executes the defined effect

Supported Conditions:

- `==`, `!=`, `>`, `<`, `>=`, `<=`

Supported Effects:

- `action`: `"open"` or `"close"`
- `target`: a single device or a list
- `message`: optional message for SCADA UI

File: `control_logic/action_engine.py`

Design Considerations
---------------------

- PLCs can be customized with local logic
- SCADA can implement fallback or safety logic
- All logic executes every tick in the simulation loop

Debugging Logic
---------------

If a rule fails, you’ll see console output like:

.. code-block::

    [ENGINE] No device found for register 5
    [MODBUS-PLC] Overwrote pump1 at register 10 with value 0