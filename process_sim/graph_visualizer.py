# process_sim/graph_visualizer.py

import networkx as nx
import matplotlib.pyplot as plt
import threading
import time

def render_live_graph(graph, interval=1.0):
    def update_loop():
        while True:
            G = nx.DiGraph()
            labels = {}

            for node_id, node in graph.nodes.items():
                label = f"{node.name}\n"
                if hasattr(node, "rate"):
                    label += f"Rate: {node.rate}"
                if hasattr(node, "current_volume"):
                    label += f"Vol: {node.current_volume}\nMax: {node.max_capacity}"
                labels[node_id] = label
                G.add_node(node_id)

            for line_id, line in graph.lines.items():
                edge_label = f"{line.name}\nBuffer: {line.buffer}"
                G.add_edge(line.source.id, line.target.id, label=edge_label)

            pos = nx.spring_layout(G, seed=42)
            plt.clf()
            nx.draw(G, pos, with_labels=True, labels=labels, node_color="lightgreen", node_size=1500)
            edge_labels = nx.get_edge_attributes(G, "label")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.pause(interval)

    threading.Thread(target=update_loop, daemon=True).start()
    plt.show()
