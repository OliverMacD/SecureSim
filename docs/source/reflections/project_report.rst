===============================
SecureSim Final Project Report
===============================

Project Overview
================
Briefly describe the purpose of the project:
- Simulate an Industrial Control System (ICS)
- Model a real-world process (water treatment)
- Implement and test cybersecurity attacks and defenses

System Architecture
===================
Outline the main system components with a diagram (if available).

.. image:: ../img/system_architecture.png
   :alt: SecureSim Architecture
   :align: center

Main folders and their roles:
- `process_sim/`: Fluid system simulation
- `control_logic/`: PLC & SCADA logic
- `attacks/`: Replay, FDI, DoS
- `defenses/`: Logging, anomaly detection, auth
- `scada_ui/`: Web interface for monitoring
- `servers/`: MQTT + Modbus

Process Modeling
================
Describe the modeled process (e.g., water treatment plant):
- Tanks 1–6: collection, treatment, output, overflow
- Splitters, pumps, and flow control
- Emergency shutdown logic (PLC + SCADA)

Include a schematic or flow diagram if possible.

Control Logic
=============
Summarize the PLC and SCADA control strategies:
- Threshold-based logic
- Emergency stop conditions
- Modbus register mappings
- SCADA interface features

Attack Implementation
=====================
Document each attack:

**Replay Attack**
- Description: Reused sensor data to hide overflow
- Implementation: Stored and resent tank readings
- Impact: Prevented alarm conditions

**Dos**
- Description: Dos Attack
- Implementation: Modified MQTT payloads
- Impact: TODO

Defense Mechanisms
==================
Describe and evaluate each defense:

**Anomaly Detection**
- Based on static thresholds or change-rate
- Detected unexpected tank level spikes

**Logging & Auditing**
- All system actions and values logged to `/data`
- Used for post-attack analysis

**Command Authentication** *(if implemented)*
- Basic command verification before action

Evaluation & Results
====================
Present evidence of attacks and defenses:
- Graphs of tank levels
- Logs of detection events
- Screenshots from the UI (Flask dashboard or CLI)

.. image:: ../img/tank_levels.png
   :alt: Tank Levels Graph

Performance:
- Detection rates
- False positives/negatives (if tested)
- Defense response times

Team Collaboration
==================
Summarize how tasks were divided:
- Who handled modeling, attacks, defenses, UI, etc.
- Tools used: GitHub, issue tracking, version control evidence

Challenges & Limitations
========================
Discuss difficulties encountered:
- MQTT/Modbus sync
- Attack timing
- UI reliability or threading issues
- Any parts that weren’t implemented as planned

Conclusions & Future Work
=========================
Summarize findings and insights:
- ICS systems are vulnerable without detection layers
- Simple defense logic can be surprisingly effective
- Realistic simulation aids security prototyping

Propose future extensions:
- ML-based detection
- Real protocol stacks (e.g., full Modbus stack)
- Real-time dashboards

Appendices
==========
- Code snippets
- System layout JSON
- Sample logs
