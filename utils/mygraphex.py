from utils.graph import *


def create_graph_n_minus_one_path(n):
    G = Graph(False, 0)
    u = Vertex(G)
    for i in range(n - 1):
        v = Vertex(G)
        f = Edge(u, v)
        G.add_edge(f)
        u = v
    print(G)
    return G


def create_graph_n_cycle(n):
    G = Graph(False, 0)
    u = Vertex(G)
    for i in range(n - 1):
        v = Vertex(G)
        f = Edge(u, v)
        G.add_edge(f)
        u = v
    f = Edge(G.vertices[n - 1], G.vertices[0])
    G.add_edge(f)
    print(G)
    return G


def create_complete_graph(n):
    G = Graph(True, n)
    for i in G.vertices:
        for j in G.vertices:
            if j.label != i.label:
                f = Edge(i, j)
                G.add_edge(f)
    print(G)
    return G


create_graph_n_minus_one_path(10)
create_graph_n_cycle(10)
create_complete_graph(4)
