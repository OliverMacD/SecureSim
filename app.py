from flask import Flask, render_template
import io
import base64
import matplotlib.pyplot as plt
from process_sim.graph_visualizer import render_process_graph

app = Flask(__name__)

@app.route("/")
def home():
    # Render the graph as an image
    graph_image = render_graph_as_image()
    return render_template("index.html", graph_image=graph_image)

def render_graph_as_image():
    from process_sim.layout_parser import load_layout

    # Load the graph from the JSON layout
    graph = load_layout("Process_sim.json")

    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 6))
    render_process_graph(graph, show_labels=True)

    # Save the figure to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    # Encode the image as a base64 string
    return base64.b64encode(buf.getvalue()).decode("utf-8")

if __name__ == "__main__":
    app.run(debug=True)