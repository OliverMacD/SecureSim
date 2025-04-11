Process Simulation Components
=============================

SecureSim simulates fluid-handling systems using modular components that represent physical devices. These are defined in the system layout and executed within the simulation engine on each tick.

Core Components
---------------

.. list-table::
   :header-rows: 1

   * - Component
     - Description
     - File
   * - **Tank**
     - Stores and receives fluid, publishes volume via MQTT.
     - ``process_sim/tank.py``
   * - **Pump**
     - Moves fluid from one tank to another through a line, with MQTT control of flow rate and state.
     - ``process_sim/pump.py``
   * - **Splitter**
     - Evenly splits incoming fluid to multiple downstream lines.
     - ``process_sim/splitter.py``
   * - **Line**
     - Represents a connection between nodes; buffers and transfers fluid.
     - ``process_sim/line.py``

Each of these components inherits from the base `ProcessComponent` class defined in ``process_sim/base.py``.

Update and Publish Cycle
------------------------

Every component supports two core methods:

- ``update()``: Advances the internal logic of the component.
- ``publish()``: Sends the current state to MQTT for visualization or control logic.

The simulation loop (in ``simulation_runner.py``) calls these methods every tick.

Interfaces
----------

All components interact through:

- **MQTT**: Used to report states and receive control messages.
- **Modbus**: Used by PLCs/SCADA for state monitoring and override logic.

See also:

.. toctree::
   :maxdepth: 1

   json_structure
   comms