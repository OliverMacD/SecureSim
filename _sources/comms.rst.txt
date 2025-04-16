Communication Interfaces
========================

SecureSim uses two industrial communication protocols:

1. **MQTT** – For telemetry and component-level control
2. **Modbus TCP** – For PLC and SCADA communication

MQTT
----

MQTT is used for real-time publish/subscribe messaging between components, PLCs, and the UI.

Each component publishes and subscribes to its own set of MQTT topics.

### Topic Structure

.. list-table::
   :header-rows: 1

   * - Topic
     - Purpose
   * - ``tank/{id}/volume``
     - Publishes current volume of a tank
   * - ``tank/{id}/max_capacity``
     - Publishes configured max capacity
   * - ``pump/{id}/state``
     - Publishes if a pump is open or closed
   * - ``pump/{id}/rate``
     - Publishes current flow rate of a pump
   * - ``set/tank/{id}/max_capacity``
     - Subscribes to override tank capacity
   * - ``set/pump/{id}/state``
     - Subscribes to open/close pump
   * - ``set/pump/{id}/rate``
     - Subscribes to update pump rate

### MQTT Backend

- Broker address: ``127.0.0.1``
- Port: ``1883``
- Handled by: ``servers/mqtt_server.py``
- Uses `gmqtt` for async communication

Modbus TCP
----------

Used by all **PLCs** and the **SCADA** system for:

- Monitoring system state
- Writing control commands to simulation components
- Performing overrides and emergency shutdowns

### Modbus Servers

Each PLC and the SCADA system runs its own Modbus TCP server.

- **PLC Ports**: `5100`, `5101`, ...
- **SCADA Port**: `5200`
- Registers mapped to devices like tanks and pumps

### Register Mapping

Registers represent real device attributes:

.. list-table::
   :header-rows: 1

   * - Device Attribute
     - Register Value
   * - ``tank.current_volume``
     - Integer approximation
   * - ``pump.state``
     - 0 = closed, 1 = open
   * - ``pump.rate``
     - Integer flow rate

### Modbus Override Behavior

When a value is written to a register:
- The system locates the target device
- Calls an appropriate setter like `set_state()` or `set_rate()`
- Overwrites the simulation state

### Implementation

- Custom server: ``servers/modbus_server.py``
- Wraps a register array and update hook
- Linked to logic in ``plc_modbus.py`` and ``scada_modbus.py``

Design Notes
------------

- Use MQTT for frequent, real-time updates (volume, state)
- Use Modbus for secure/controlled writes or HMI emulation
- SCADA and PLCs can use both interfaces simultaneously