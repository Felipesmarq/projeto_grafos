import pytest
from graphs.graph import Graph
from graphs.algorithms import dijkstra

def test_dijkstra_standard_logic():
    g = Graph(directed=True)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)

    g.add_edge(1, 2, 2)
    g.add_edge(1, 3, 5)
    g.add_edge(2, 3, 1)

    custo, caminho = dijkstra(g, 1, 3)

    assert custo == 3
    assert caminho == [1, 2, 3]


def test_dijkstra_rejects_negative_weights():

    g = Graph(directed=True)
    g.add_node(1)
    g.add_node(2)

    g.add_edge(1, 2, -5)

    with pytest.raises(ValueError) as excinfo:
        dijkstra(g, 1, 2)
    
    assert "não aceita" in str(excinfo.value)


def test_dijkstra_no_path():
    g = Graph(directed=True)
    g.add_node(1)
    g.add_node(2)

    custo, caminho = dijkstra(g, 1, 2)

    assert custo == float("inf")
    assert caminho == []