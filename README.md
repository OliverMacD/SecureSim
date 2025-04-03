# secure-sim: Industrial Control System Simulation

This project simulates a simplified **Industrial Control System (ICS)** in Python, designed for educational purposes in cybersecurity. It includes a modeled process, simulated devices (PLCs, RTUs, and SCADA), realistic cyberattacks, and integrated defenses. The system is fully software-based with no physical hardware requirements.

---

## 🚀 Project Overview

The **secure-sim** project provides a modular simulation of a basic industrial process (TBD), emulating real-world ICS architecture. It includes:

- **Process Modeling**: Simulated sensors, actuators, and control logic.
- **Cybersecurity Features**: Demonstration of attacks and countermeasures.
- **Interactive UI**: A web-based dashboard for monitoring, attack execution, and defense toggling.
- **Modular Code Structure**: All devices and components are built as independent, concurrent Python processes.

---

## 🧠 Simulated Architecture

- **PLC Devices**: Contain control logic for managing actuators based on sensor data.
- **SCADA Server**: Collects and displays system state, sends commands to PLCs, and logs data.
- **All devices (PLCs & SCADA)** run as **independent processes**.
- **Streamlit UI**: Central user interface for real-time system monitoring and security management.

---

## 🔐 Simulated Attacks

Three common ICS attacks are implemented in the simulation:

- **Replay Attack**: Records legitimate data and replays it to hide anomalies.
- **False Data Injection**: Sends fake sensor or actuator data to disrupt system behavior.
- **Denial of Service (DoS)**: Overwhelms the system with traffic to degrade performance or disable components.

Each attack can be launched and stopped through the Streamlit UI.

---

## 🛡️ Security Defenses

The following defenses are implemented:

- **Logging and Auditing**: All device communications and key events are logged to files in the `data/` folder.
- **Authentication**: Basic command authentication is supported for controlling devices.
- **Anomaly Detection**: Monitors system data for deviations from expected behavior.

All defenses can be enabled or disabled dynamically through the UI.

---

## 📁 Folder Structure

```
secure-sim/
├── process_sim/           # Simulated plant and environment models
├── control_logic/         # PLCs and SCADA logic/ devices
├── scada_ui/              # Streamlit UI for monitoring and control
├── attacks/               # Attack modules (Replay, FDI, DoS)
├── defenses/              # Logging, authentication, anomaly detection
├── tests/                 # Test cases and unit tests
├── data/                  # Logs, system outputs, detection results
├── servers/               # ModBus & MQTT Server initializers
├── docs/                  # Docs for system features
├── main.py                # Entry point to start the full simulation
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

---

## 🧪 How to Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the simulation**:
   ```bash
   python main.py
   ```

3. **Access the UI**:
   - Open your browser and go to the local Streamlit server address (usually http://localhost:8501).

---

## 📊 Visualization

- Live plots and logs of sensor data, actuator states, and attack/defense status.
- System metrics visualized using `matplotlib` or `plotly`.
- All outputs stored to the `data/` folder for future analysis.

---

## 📓 Deliverables

- Source code (Python 3)
- Final written report (with visualizations and logs)
- Group presentation (7–10 minutes)
- Individual reflection paper (1 page max)

---

## 🛠 Technologies

- Python 3
- Streamlit (UI)
- threading / multiprocessing (device simulation)
- logging module (defense & audit)
- matplotlib / plotly (visualization)
