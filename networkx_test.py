# networkx_tutorial.py
import networkx as nx
import matplotlib.pyplot as plt

def build_sample_graph():
    G = nx.Graph()
    # add some nodes
    G.add_nodes_from(["A", "B", "C", "D"])
    # add weighted edges
    G.add_edge("A", "B", weight=4)
    G.add_edge("A", "C", weight=1)
    G.add_edge("C", "B", weight=2)
    G.add_edge("B", "D", weight=5)
    G.add_edge("C", "D", weight=8)
    return G

def show_graph(G, highlight_path=None):
    pos = nx.spring_layout(G)  # or any layout you like
    # draw all edges
    nx.draw(G, pos, with_labels=True)
    # draw edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # if you pass in a list of nodes for a path, highlight it
    if highlight_path:
        path_edges = list(zip(highlight_path, highlight_path[1:]))
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            width=3,
            edge_color='red'
        )
    plt.show()

def main():
    G = build_sample_graph()
    print("Nodes:", G.nodes())
    print("Edges with weights:", G.edges(data=True))

    # compute shortest path from A to D
    path = nx.dijkstra_path(G, source="A", target="D", weight='weight')
    print("Shortest path A→D:", path)

    show_graph(G, highlight_path=path)

if __name__ == "__main__":
    main()
