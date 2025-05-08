import networkx as nx

def compute_mst(graph):
    
    return nx.minimum_spanning_tree(graph, algorithm="prim")