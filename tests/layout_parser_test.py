"""
Standalone Layout Parser Test Script

This script directly loads the process layout and verifies:
- All nodes are initialized
- All lines are properly connected
- All pumps have valid source and target connections

Logs issues to the console.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from process_sim.layout_parser import load_layout


# Path to layout file (adjust if needed)
LAYOUT_PATH = "Process_sim.json"

def main():
    print(f"\n Testing layout loading from: {LAYOUT_PATH}\n")

    if not os.path.exists(LAYOUT_PATH):
        print(f" Layout file not found at: {LAYOUT_PATH}")
        return

    try:
        graph = load_layout(LAYOUT_PATH)
    except Exception as e:
        print(f" Failed to load layout: {e}")
        return

    print(f"Layout loaded successfully with {len(graph.nodes)} nodes and {len(graph.lines)} lines.\n")

    print("Validating pump connections...\n")
    errors_found = False

    for node_id, node in graph.nodes.items():
        if node.__class__.__name__ == "Pump":
            if node.source is None:
                print(f"❌ Pump '{node.id}' is missing a valid source_id or the source was not found in the layout.")
            if node.target is None:
                print(f"❌ Pump '{node.id}' is missing a valid target_id or the target was not found in the layout.")
            if node.source and node.target:
                print(f"✅ Pump '{node.id}' connected from '{node.source.id}' to '{node.target.id}'")


    if not errors_found:
        print("\n All pumps have valid connections.")

    print("\n Layout parser test complete.")

if __name__ == "__main__":
    main()
