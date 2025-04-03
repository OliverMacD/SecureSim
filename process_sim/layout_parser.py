# process_sim/layout_parser.py

import json
from process_sim.tank import Tank
from process_sim.pump import Pump
from process_sim.splitter import Splitter
from process_sim.line import Line

class ProcessGraph:
    def __init__(self):
        self.nodes = {}
        self.lines = {}

    def update(self):
        for node in self.nodes.values():
            node.update()
        for line in self.lines.values():
            line.update()

    def publish(self):
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
    with open(json_path, 'r') as f:
        layout = json.load(f)

    graph = ProcessGraph()

    # First pass: create nodes
    for node in layout["nodes"]:
        node_id = node["id"]
        node_type = node["type"]
        name = node["name"]

        if node_type == "Tank":
            max_capacity = node.get("max_capacity", 1000)
            initial_capacity = node.get("initial_capacity", 0)
            tank = Tank(node_id, name, max_capacity)
            tank.current_volume = initial_capacity
            graph.nodes[node_id] = tank

        elif node_type == "Pump":
            flow_rate = node.get("flow_rate", 10)
            pump = Pump(node_id, name, flow_rate)
            pump.source_id = node.get("source")  # We'll resolve this later
            graph.nodes[node_id] = pump

        elif node_type == "Splitter":
            splitter = Splitter(node_id, name)
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

        # Register connections
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

    return graph