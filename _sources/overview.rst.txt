System Overview
===============

SecureSim is a modular simulation platform for modeling Industrial Control Systems (ICS) using Python.
It simulates a realistic fluid-based process system with support for PLCs, SCADA, MQTT, Modbus,
cyberattacks, and a real-time UI.

Features
--------

- 🏭 **Process Simulation** — Model tanks, pumps, splitters, and fluid flow
- ⚙️ **PLCs & SCADA** — Custom logic via register-based rules and Modbus
- 📡 **MQTT + Modbus** — Realistic communication stack for sensors and control
- 🛡️ **Attack & Defense** — Built-in support for replay, DoS, and FDI attacks
- 🖥️ **Streamlit UI** — Real-time system monitoring and security toggles
- 📈 **Graph Visualization** — Live network view of the entire system

Folder Structure
----------------

.. code-block:: text

    secure-sim/
    ├── main.py                   # Launches the simulation and UI
    ├── Process_sim.json          # System layout and logic
    │
    ├── process_sim/              # Core simulation engine
    │   ├── base.py, tank.py, pump.py, splitter.py, line.py
    │   ├── layout_parser.py, simulation_runner.py
    │   ├── graph_visualizer.py
    │   └── interfaces/mqtt_interface.py
    │
    ├── control_logic/            # PLCs, SCADA, and action engine
    │   ├── plc.py, plc_modbus.py
    │   ├── scada.py, scada_modbus.py
    │   └── action_engine.py
    │
    ├── servers/                  # Communication servers
    │   ├── mqtt_server.py
    │   └── modbus_server.py
    │
    ├── scada_ui/                 # Streamlit dashboard
    ├── attacks/                  # Attack modules
    ├── defenses/                 # Logging, auth, detection
    ├── tests/                    # MQTT + pump test scripts
    ├── docs/                     # Sphinx documentation source
    ├── data/                     # Logging and system outputs
    ├── requirements.txt          # Python dependencies
    └── README.md                 # Project overview

Documentation
-------------

Build docs using Sphinx:

.. code-block:: bash

    cd docs
    sphinx-build -b html source build/html

Then open ``build/html/index.html``.

Simulation Overview
-------------------

The system models a **water treatment process**:

+---------------------+---------------------------------------------+
| Stage               | Description                                 |
+=====================+=============================================+
| Waste Collection    | Tank 1 holds incoming wastewater            |
+---------------------+---------------------------------------------+
| Chemical Treatment  | Pumps draw from Tanks 3 & 4 into Tank 2     |
+---------------------+---------------------------------------------+
| Clean Output        | Tank 2 drains into Splitter → Tanks 5 & 6   |
+---------------------+---------------------------------------------+
| Overflow Return     | Tanks 5/6 pump back to Tank 1 if overflow   |
+---------------------+---------------------------------------------+
| Emergency Stop      | SCADA closes all pumps via register 99      |
+---------------------+---------------------------------------------+

Security Features
-----------------

+------------------------+------------------------------------------+
| Attack                 | Description                              |
+========================+==========================================+
| Replay Attack          | Repeats recorded data to mask changes    |
+------------------------+------------------------------------------+
| False Data Injection   | Modifies sensor or control values        |
+------------------------+------------------------------------------+
| Denial of Service      | Overloads communication channels         |
+------------------------+------------------------------------------+

+------------------------+------------------------------------------+
| Defense                | Description                              |
+========================+==========================================+
| Anomaly Detection      | Flags abnormal behavior patterns         |
+------------------------+------------------------------------------+
| Logging & Auditing     | System events saved to `/data`           |
+------------------------+------------------------------------------+
| Command Authentication | Verifies actions before execution        |
+------------------------+------------------------------------------+

Testing Tools
-------------

.. code-block:: bash

    python tests/mqtt_broker_test.py
    python tests/pump_control_test.py

Extendability
-------------

- Add new component types by subclassing `ProcessComponent`
- Add new PLC logic via `plc_modbus.py`
- Add SCADA rules in `scada_modbus.py`
- Customize UI under `scada_ui/`