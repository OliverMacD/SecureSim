"""
Process Layout Parser and Graph Builder

This module parses a JSON layout definition and constructs a simulation graph
of interconnected components including tanks, pumps, splitters, and lines.
It also initializes MQTT interfaces and binds Modbus/SCADA control paths.

Classes:
    ProcessGraph - Container for simulation nodes and lines with update/publish hooks.

Functions:
    load_layout - Loads and parses a JSON layout file to construct a ProcessGraph.
"""

import json
from process_sim.tank import Tank
from process_sim.pump import Pump
from process_sim.splitter import Splitter
from process_sim.line import Line
from process_sim.interfaces.mqtt_interface import MQTTInterface


class ProcessGraph:
    """
    Holds all process components (nodes) and connections (lines) in the simulation.
    Handles update and publish cycles for the entire graph.
    """

    def __init__(self):
        self.nodes = {}         # node_id -> component instance
        self.lines = {}         # line_id -> Line instance
        self.plc_configs = []   # List of PLC configurations
        self.scada_config = None  # SCADA configuration dictionary

    def update(self):
        """Runs the update logic for all nodes and lines in the graph."""
        for node in self.nodes.values():
            node.update()
        for line in self.lines.values():
            line.update()

    def publish(self):
        """Triggers data publication for all nodes and lines."""
        for node in self.nodes.values():
            try:
                node.publish()
            except Exception as e:
                print(f"[ERROR] Failed to publish node {node.id} ({node.name}): {e}")

        for line in self.lines.values():
            try:
                line.publish()
            except Exception as e:
                print(f"[ERROR] Failed to publish line {line.id} ({line.name}): {e}")


def load_layout(json_path):
    """
    Loads a process layout from a JSON file and constructs a ProcessGraph.

    The JSON file must include:
      - nodes: list of component definitions (Tanks, Pumps, Splitters)
      - edges: list of connections between components
      - plcs: (optional) list of PLC configuration dictionaries
      - scada: (optional) SCADA configuration dictionary

    Args:
        json_path (str): Path to the layout JSON file.

    Returns:
        ProcessGraph: The fully constructed and connected graph.
    """
    with open(json_path, 'r') as f:
        layout = json.load(f)

    graph = ProcessGraph()

    # First pass: create nodes
    for node in layout["nodes"]:
        node_id = node["id"]
        node_type = node["type"]
        name = node["name"]
        position = node.get("position")

        mqtt_interface = MQTTInterface(client_id=f"{node_type.lower()}_{node_id}")

        if node_type == "Tank":
            max_capacity = node.get("max_capacity", 1000)
            initial_capacity = node.get("initial_capacity", 0)
            tank = Tank(node_id, name, max_capacity, mqtt_interface=mqtt_interface)
            tank.current_volume = initial_capacity
            if position:
                tank.position = position
            graph.nodes[node_id] = tank

        elif node_type == "Pump":
            flow_rate = node.get("flow_rate", 10)
            is_open = node.get("is_open", True)
            pump = Pump(node_id, name, flow_rate, mqtt_interface=mqtt_interface, is_open=is_open)
            pump.source_id = node.get("source")
            if position:
                pump.position = position
            graph.nodes[node_id] = pump

        elif node_type == "Splitter":
            splitter = Splitter(node_id, name)
            if position:
                splitter.position = position
            graph.nodes[node_id] = splitter

    # Second pass: create lines and connect nodes
    for edge in layout["edges"]:
        edge_id = edge["id"]
        name = edge["name"]
        source_id = edge["source"]
        target_id = edge["target"]

        line = Line(edge_id, name)
        graph.lines[edge_id] = line

        source = graph.nodes.get(source_id)
        target = graph.nodes.get(target_id)
        line.source = source
        line.target = target

        if isinstance(source, Tank):
            source.add_output(line)
        elif isinstance(source, Pump):
            source.set_connection(None, line)
        elif isinstance(source, Splitter):
            source.add_output(line)

        if isinstance(target, Tank):
            target.add_input(line)

    # Third pass: resolve pump sources
    for node in graph.nodes.values():
        if isinstance(node, Pump) and hasattr(node, "source_id"):
            source_node = graph.nodes.get(node.source_id)
            if source_node:
                node.source = source_node

    # Load optional controller configurations
    graph.plc_configs = layout.get("plcs", [])
    graph.scada_config = layout.get("scada", {})

    return graph
