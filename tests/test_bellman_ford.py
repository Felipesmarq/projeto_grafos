from graphs.graph import Graph
from graphs.algorithms import bellman_ford

def test_bellman_ford_negative_weights_without_cycle():
    g = Graph(directed=True)
    
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)

    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, -2)
    g.add_edge(1, 3, 4)

    custo, caminho = bellman_ford(g, 1, 3)

    assert custo == -1
    assert caminho == [1, 2, 3]


def test_bellman_ford_detects_negative_cycle():
    g = Graph(directed=True)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)

    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, -2)
    g.add_edge(3, 1, -2) 

    custo, caminho = bellman_ford(g, 1, 3)

    assert custo == float("-inf")
    assert caminho == []