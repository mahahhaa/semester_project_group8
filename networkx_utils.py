import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Coordinates: node -> (latitude, longitude)
coords = {
    "Eastside South Parking Structure": (33.880339247188815, -117.88174527889755),
    "Eastside North Parking Structure": (33.88106221519995, -117.88179166935485),
    "Nutwood Parking Structure": (33.87911777106525, -117.88851568364892),
    "State College Parking Structure": (33.88312182794434, -117.88860048226113),
    "CSUF - Lot A": (33.887399484126604, -117.88877382879025),
    "CSUF - Lot G": (33.88842371183974, -117.88659051067648),

    "Computer Science Building": (33.88246112207914, -117.88268234576192),
    "Engineering Building": (33.88237108879833, -117.8832214053826),
    "Student Health & Counseling Center": (33.883039868123966, -117.88426233597886),
    "Titan Gymnasium": (33.88317593161453, -117.88605608964025),
    "Student Recreation Center": (33.883184914793425, -117.88778273469337),
    "Titan Student Union": (33.881889089000694, -117.88846625694629),
    "Titan Shops": (33.881948546296215, -117.88687212364808),
    "Pollak Library": (33.881324672810365, -117.88526941639248),
    "Education-Classroom": (33.88132097935114, -117.8843558224976),
    "Humanities Building": (33.88046564790404, -117.88419952711486),
    "Gordon Hall": (33.87973930585969, -117.88416639959854),
    "Langsdorf Hall": (33.879048143538164, -117.88449493891623),
    "Dan Black Hall": (33.879178121163726, -117.88580379293649),
    "McCarthy Hall": (33.879732595029274, -117.88550606774095),
    "Clayes Performing Arts Center": (33.88056756135152, -117.88670313385623),
}

# Category mapping: node -> category
node_category = {
    # Parking lots
    **{name: 'Parking' for name in [
        'Eastside South Parking Structure',
        'Eastside North Parking Structure',
        'Nutwood Parking Structure',
        'State College Parking Structure',
        'CSUF - Lot A',
        'CSUF - Lot G'
    ]},
    # Academic buildings
    **{name: 'Academic' for name in [
        'Computer Science Building',
        'Engineering Building',
        'Pollak Library',
        'Education-Classroom',
        'Humanities Building',
        'Gordon Hall',
        'Langsdorf Hall',
        'Dan Black Hall',
        'McCarthy Hall',
        'Clayes Performing Arts Center',
        'Titan Gymnasium',
        'Student Recreation Center'
    ]},
    # Student Services
    **{name: 'Student Services' for name in [
        'Student Health & Counseling Center',
        'Titan Student Union',
        'Titan Shops'
    ]}
}

# Style mapping: category -> drawing style
category_style = {
    'Parking':          {'color': 'gray',      'shape': 's'},
    'Academic':         {'color': 'skyblue',   'shape': 'o'},
    'Student Services': {'color': 'gold',      'shape': 'D'}
}

# Define edges between directly connected buildings (sample based on campus map)
edge_list = [
    # Parking loop
    ('Eastside South Parking Structure', 'Eastside North Parking Structure'),
    ('Eastside North Parking Structure', 'Education-Classroom'),
    ('Eastside North Parking Structure', 'Computer Science Building'),
    
    ('Eastside South Parking Structure', 'Gordon Hall'),
    
    ('Computer Science Building', 'Engineering Building'),
    
    ('Engineering Building', 'Student Health & Counseling Center'),
    ('Engineering Building', 'Education-Classroom'),
    
    ('Student Health & Counseling Center', 'Titan Gymnasium'),
    ('Student Health & Counseling Center', 'Education-Classroom'),
    ('Student Health & Counseling Center', 'Pollak Library'),
    
    ('Pollak Library', 'Titan Gymnasium'),
    ('Pollak Library', 'Titan Shops'),
    ('Pollak Library', 'Clayes Performing Arts Center'),
    ('Pollak Library', 'McCarthy Hall'),
    ('Pollak Library', 'Humanities Building'),
    ('Pollak Library', 'Education-Classroom'),
    
    ('Titan Gymnasium', 'Titan Shops'),    
    ('Titan Gymnasium', 'Student Recreation Center'),
    ('Titan Gymnasium', 'CSUF - Lot A'),
    ('Titan Gymnasium', 'CSUF - Lot G'),
    
    ('Titan Shops', 'Titan Student Union'),
    ('Titan Shops', 'Student Recreation Center'),
    ('Titan Shops', 'Clayes Performing Arts Center'),
    
    ('Clayes Performing Arts Center', 'McCarthy Hall'),
    ('Clayes Performing Arts Center', 'Titan Student Union'),
    ('Clayes Performing Arts Center', 'Nutwood Parking Structure'),
    ('Clayes Performing Arts Center', 'McCarthy Hall'),
    ('Clayes Performing Arts Center', 'Humanities Building'),
    
    ('Humanities Building', 'Gordon Hall'),
    ('Humanities Building', 'McCarthy Hall'),
    
    ('Gordon Hall', 'Langsdorf Hall'),
    ('Gordon Hall', 'Dan Black Hall'),
    ('Gordon Hall', 'McCarthy Hall'),
    
    ('McCarthy Hall', 'Langsdorf Hall'),
    
    ('Dan Black Hall', 'Langsdorf Hall'),
    ('Dan Black Hall', 'McCarthy Hall'),
    
    ('Nutwood Parking Structure', 'Dan Black Hall'),
    ('Nutwood Parking Structure', 'McCarthy Hall'),
    ('Nutwood Parking Structure', 'Titan Student Union'),

    ('Titan Student Union', 'Student Recreation Center'),
    
    ('State College Parking Structure', 'Student Recreation Center'),
    ('State College Parking Structure', 'Titan Gymnasium'),
    ('State College Parking Structure', 'Titan Student Union'),
    
    ('CSUF - Lot A', 'Student Recreation Center'),
    ('CSUF - Lot A', 'State College Parking Structure'),
    ('CSUF - Lot A', 'CSUF - Lot G'),
    
    ('CSUF - Lot G', 'Student Health & Counseling Center'),
]

def build_graph():
    """
    Constructs a graph with nodes at real geo-coordinates
    and edges weighted by geodesic distance.
    """
    G = nx.Graph()
    # Add all nodes
    for node in coords:
        G.add_node(node)

    # Add edges with true distance weights
    for u, v in edge_list:
        dist_m = geodesic(coords[u], coords[v]).meters
        G.add_edge(u, v, weight=dist_m)

    return G

def draw_graph(graph, highlight_path=None, background_image=None):
    """
    Draws the graph using geographic positions and colored by category.
    Returns a Matplotlib Figure.
    """
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    
    # Compute scaled positions from lat/lon
    lats = [lat for lat, lon in coords.values()]
    lons = [lon for lat, lon in coords.values()]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    pos = {node: ((lon - min_lon)*100000, (lat - min_lat)*100000)
           for node, (lat, lon) in coords.items()}

    # Draw nodes by category
    for cat, style in category_style.items():
        nodelist = [n for n, c in node_category.items() if c == cat]
        nx.draw_networkx_nodes(graph, pos, nodelist=nodelist,
                               node_color=style['color'], node_shape=style['shape'],
                               node_size=150, label=cat, ax=ax)
    ax.legend(title='Category')

    # Draw edges and weight labels
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color='gray')
    weights = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos,
                                 edge_labels={k: f"{v:.0f}m" for k, v in weights.items()},
                                 ax=ax)

    # Highlight path if provided
    if highlight_path:
        path_edges = list(zip(highlight_path, highlight_path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges,
                               width=4, edge_color='red', ax=ax)
    return fig

def draw_mst(graph, mst_edges):
    """
    Draws the minimum spanning tree edges on the same geographic layout.
    """
    fig, ax = plt.subplots(figsize=(14, 7), dpi=80)
    # Recompute scaled positions inside this function
    lats = [lat for lat, lon in coords.values()]
    lons = [lon for lat, lon in coords.values()]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    pos = {node: ((lon - min_lon)*100000, (lat - min_lat)*100000)
           for node, (lat, lon) in coords.items()}

    # Draw base nodes and all edges faintly
    nx.draw_networkx_nodes(graph, pos, node_size=300, ax=ax)
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color='lightgray')

    # Highlight MST edges prominently
    nx.draw_networkx_edges(graph, pos, edgelist=mst_edges,
                           ax=ax, edge_color='green', width=3)

    # Draw labels on top
    nx.draw_networkx_labels(graph, pos, ax=ax)
    return fig
