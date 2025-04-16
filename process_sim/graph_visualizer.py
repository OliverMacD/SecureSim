"""
Process Graph Visualization

This module provides static and live visualizations of a process simulation graph
using NetworkX and matplotlib. It supports rendering node connections, names, and
live data such as rates, volumes, and state.

Functions:
    render_process_graph - Displays a labeled, static process graph layout.
    render_live_graph - Continuously updates the graph with live simulation values.
"""

import networkx as nx
import matplotlib.pyplot as plt

def render_process_graph(graph, show_labels=True):
    """
    Render a static diagram of the simulation graph using node names and edge labels.

    Args:
        graph (ProcessGraph): The simulation graph containing nodes and lines.
        show_labels (bool): Whether to show node names.
    """
    G = nx.DiGraph()
    pos = {}

    # Add nodes and record positions
    for node_id, node in graph.nodes.items():
        G.add_node(node_id, label=node.name)
        if hasattr(node, "position"):
            pos[node_id] = tuple(node.position)

    # Add edges
    for line_id, line in graph.lines.items():
        G.add_edge(line.source.id, line.target.id, label=line.name)

    # Use spring layout if positions are missing
    if len(pos) < len(graph.nodes):
        pos = nx.spring_layout(G, seed=42)

    # Draw the graph
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
    Continuously update and display the graph showing live simulation data
    such as tank volumes, pump rates, and open/closed states.

    Args:
        graph (ProcessGraph): The simulation graph to monitor.
        interval (float): Time delay (in seconds) between graph updates.
    """
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))

    while True:
        ax.clear()

        G = nx.DiGraph()
        labels = {}
        pos = {}

        # Build node data with dynamic labels
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

        # Add edges
        for line_id, line in graph.lines.items():
            G.add_edge(line.source.id, line.target.id)

        if len(pos) < len(graph.nodes):
            pos = nx.spring_layout(G, seed=42)

        nx.draw(G, pos, ax=ax, with_labels=True, labels=labels,
                node_size=1500, node_color="lightgreen", arrows=True)

        edge_labels = nx.get_edge_attributes(G, "label")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        ax.set_title("Live Process Graph")
        plt.draw()
        plt.pause(interval)
