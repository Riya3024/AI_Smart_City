import networkx as nx

def get_route(start, end):
    G = nx.Graph()
    G.add_weighted_edges_from([
        ("Gate", "Library", 5),
        ("Library", "Cafeteria", 3),
        ("Cafeteria", "Hostel", 4),
        ("Gate", "Hostel", 10)
    ])
    return nx.shortest_path(G, start, end, weight="weight")