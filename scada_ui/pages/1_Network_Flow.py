# scada_ui/pages/2_Assumed_Network_Flow.py

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from utils.layout_loader import load_layout, get_graph_data
from utils.modbus_client import read_modbus_register

st.title("🧭 Network Flow (Modbus Data)")

layout = load_layout()
nodes, edges = get_graph_data(layout)

G = nx.DiGraph()
G.add_nodes_from(nodes.keys())
for src, tgt, _ in edges:
    G.add_edge(src, tgt)

pos = nx.spring_layout(G)

plt.figure(figsize=(12, 6))
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000)
for node_id in G.nodes:
    value = read_modbus_register("localhost", 5200, 0 if "tank" in node_id else 1)
    if value is not None:
        plt.text(pos[node_id][0], pos[node_id][1] + 0.1, f"Val: {value}", fontsize=10, ha='center')

st.pyplot(plt)
