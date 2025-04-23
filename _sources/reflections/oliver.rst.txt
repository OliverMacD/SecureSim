============================
Reflection: Oliver MacDonald
============================

Project Role & Responsibilities
-------------------------------
In this project, I focused primarily on developing the core process simulation and building out the user interface. My contributions included implementing the simulation framework for tanks, pumps, and flow lines, as well as designing and connecting the Flask-based SCADA dashboard. I was also responsible for integrating MQTT and Modbus communication layers and setting up the Sphinx documentation pipeline used to publish the project's technical resources.

Skills Developed
----------------
Through SecureSim, I deepened my understanding of Python-based communication protocols and web interfaces for industrial systems. I gained practical experience with:

- MQTT in Python for real-time telemetry
- Implementing a custom Modbus server for control logic
- Using Python’s `logging` module for auditing
- Building protected web dashboards using Flask

Beyond technical development, I also improved my skills in documentation management and project structuring through Sphinx and GitHub Actions.

Challenges Faced
----------------
A key challenge in this project was achieving reliable synchronization between MQTT messages and Modbus register updates, especially under high communication loads. Additionally, ensuring that the UI remained responsive while live data streamed in from multiple sources required careful threading and design considerations.

Lessons Learned
---------------
This project significantly expanded my understanding of both ICS architecture and cybersecurity best practices. I saw firsthand how lightweight attacks can bypass naive defenses, and how layered strategies, like authentication, logging, and rate limiting, can mitigate their impact. It reinforced the importance of simulation and structured testing in developing resilient control systems. Most importantly, I developed a more nuanced awareness of the security trade-offs inherent in designing real-time interfaces for industrial systems.

Future Applications
-------------------
The skills and insights gained through SecureSim are already being applied in my own work. I run a company building SaaS platforms, and I now approach platform architecture with a stronger focus on secure communication, auditing, and failure tolerance. Beyond that, this project has laid the foundation for my future research in cyber-physical security and human-centered interfaces for industrial systems.
