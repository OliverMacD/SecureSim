Running the Simulation
======================

This guide explains how to start the SecureSim simulation and interface with the system.

Setup Instructions
------------------

1. **Install Python dependencies**

   Use pip to install required packages:

   .. code-block:: bash

       pip install -r requirements.txt

2. **Start the simulation**

   Run the entry-point script:

   .. code-block:: bash

       python main.py

   This will:

   - Start the MQTT broker
   - Parse the `Process_sim.json` file
   - Launch the simulation thread
   - Open the Streamlit dashboard at `http://localhost:8501`

3. **View the dashboard**

   After launching, navigate in your browser to:

   .. code-block::

       http://localhost:8501

   The dashboard displays real-time information:

   - Tank volumes
   - Pump states
   - Simulation controls
   - Toggleable attacks and defenses
   - Live data visualization

Simulation Files
----------------

- **main.py**: Orchestrates the simulation, UI, and communication services
- **Process_sim.json**: Defines the system layout (nodes, edges, logic)
- **Streamlit UI**: Located in `scada_ui/`, renders live dashboards

Stopping the Simulation
-----------------------

To stop SecureSim:

- Use `Ctrl + C` in the terminal running `main.py`
- Or stop the Python process if running in an IDE

Optional: Build Sphinx Documentation
------------------------------------

If you'd like to view the system documentation:

.. code-block:: bash

    cd docs
    sphinx-build -b html source build/html
    open build/html/index.html