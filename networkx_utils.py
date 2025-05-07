import networkx as nx
import matplotlib.pyplot as plt

def build_graph():
    """
    Builds and returns the campus graph as a NetworkX Graph.
    Modify this function to define nodes and weighted edges.
    """
    G = nx.Graph()
    # TODO: replace with actual campus nodes
    G.add_node("Titan Hall")
    G.add_node("Library")
    G.add_node("Nutwood Parking Structure")
    # TODO: replace with actual campus edges and weights
    G.add_edge("Titan Hall", "Library", weight=4)
    G.add_edge("Library", "Nutwood Parking Structure", weight=6)
    return G


def draw_graph(graph, highlight_path=None):
    """
    Draws the given graph into a new Matplotlib figure.
    If highlight_path is provided (list of nodes), highlights that path.
    Returns the Matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    # 1. Compute layout positions
    pos = nx.spring_layout(graph)

    # 2. Draw base graph
    nx.draw(graph, pos, ax=ax, with_labels=True, node_size=300, font_size=8)

    # 3. Draw edge weight labels
    weights = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights, ax=ax, font_size=7)

    # 4. Highlight path if given
    if highlight_path:
        path_edges = list(zip(highlight_path, highlight_path[1:]))
        nx.draw_networkx_edges(
            graph, pos,
            edgelist=path_edges,
            ax=ax,
            width=3,
            edge_color='red'
        )

    return fig
