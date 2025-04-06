# process_sim/graph_visualizer.py

import networkx as nx
import matplotlib.pyplot as plt

def render_process_graph(graph, show_labels=True):
    G = nx.DiGraph()
    pos = {}

    for node_id, node in graph.nodes.items():
        G.add_node(node_id, label=node.name)
        if hasattr(node, "position"):
            pos[node_id] = tuple(node.position)

    for line_id, line in graph.lines.items():
        G.add_edge(line.source.id, line.target.id, label=line.name)

    # Fallback to spring layout if any position is missing
    if len(pos) < len(graph.nodes):
        pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=show_labels, node_size=1500,
            node_color="lightblue", arrows=True)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Process Flow Diagram")
    plt.tight_layout()
    plt.show()

def render_live_graph(graph, interval=1.0):
    """
    Continuously update the process graph with live simulation values.
    Node labels show dynamic data like tank volume, pump rate, etc.
    """
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))

    while True:
        ax.clear()

        G = nx.DiGraph()
        labels = {}
        pos = {}

        for node_id, node in graph.nodes.items():
            G.add_node(node_id)
            label = f"{node.name}\n"

            if hasattr(node, "rate"):
                label += f"Rate: {node.rate}\n"
            if hasattr(node, "current_volume"):
                label += f"Vol: {node.current_volume:.1f}/{node.max_capacity:.1f}"
            if hasattr(node, "is_open"):
                label += f"State: {node.is_open}"

            labels[node_id] = label

            if hasattr(node, "position"):
                pos[node_id] = tuple(node.position)

        for line_id, line in graph.lines.items():
            G.add_edge(line.source.id, line.target.id)

        # Fallback layout
        if len(pos) < len(graph.nodes):
            pos = nx.spring_layout(G, seed=42)

        nx.draw(G, pos, ax=ax, with_labels=True, labels=labels,
                node_size=1500, node_color="lightgreen", arrows=True)

        edge_labels = nx.get_edge_attributes(G, "label")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        ax.set_title("Live Process Graph")
        plt.draw()
        plt.pause(interval)