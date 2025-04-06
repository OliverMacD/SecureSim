# Expose key modules and components for easier imports
from process_sim import (
    ProcessComponent,
    Tank,
    Pump,
    Splitter,
    Line,
    load_layout,
    ProcessGraph,
    render_process_graph,
    render_live_graph,
    SimulationThread,
    MQTTInterface
)

from control_logic import (
    PLC_Template,
    scada
)

from attacks import (
    DoS,
    FalseData,
    Replay
)

# from defences import (
#     # Add specific defense modules here when implemented
# )

# Metadata for the package
__version__ = "1.0.0"
__author__ = "Oliver MacDonald"
__license__ = "MIT"