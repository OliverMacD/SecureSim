# scada_ui/pages/3_Actual_Network_Flow.py

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import time
from process_sim.interfaces.mqtt_interface import subscribe_mqtt, init_mqtt

st.set_page_config(layout="wide")
st.title("🛰 Actual Network Flow (Live MQTT Data)")

# ============ Load Layout ============
LAYOUT_PATH = "example_layout.json"

@st.cache_data
def load_layout(path):
    with open(path) as f:
        return json.load(f)

layout = load_layout(LAYOUT_PATH)
nodes = {n["id"]: n for n in layout["nodes"]}
edges = layout["edges"]

# ============ MQTT Setup =============
mqtt_values = {}

def make_callback(node_id):
    def cb(payload):
        mqtt_values[node_id] = payload
    return cb

init_mqtt()
for plc in layout.get("plcs", []):
    for device in plc["devices"]:
        topic = device["mqtt_topic"]
        node_id = device["id"]
        subscribe_mqtt(topic, make_callback(node_id))

# ============ Build Graph ============
G = nx.DiGraph()
G.add_nodes_from(nodes.keys())
for edge in edges:
    G.add_edge(edge["source"], edge["target"])

# ============ Draw Graph ============
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(12, 7))
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=10)

# Annotate with values
for node_id in G.nodes:
    val = mqtt_values.get(node_id, "...")
    plt.text(pos[node_id][0], pos[node_id][1] + 0.1, f"{node_id}: {val}", fontsize=9, ha='center', color="black")

st.pyplot(plt)
