# scada_ui/utils/layout_loader.py

import json
import os

def load_layout(path="example_layout.json"):
    if not os.path.exists(path):
        raise FileNotFoundError("Layout file not found.")
    with open(path) as f:
        return json.load(f)

def get_graph_data(layout):
    nodes = {n["id"]: n["name"] for n in layout["nodes"]}
    edges = [(e["source"], e["target"], e["name"]) for e in layout["edges"]]
    return nodes, edges
