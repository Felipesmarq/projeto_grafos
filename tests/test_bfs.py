from graphs.graph import Graph
from graphs.algorithms import bfs

def test_bfs_levels():
    g = Graph(directed=False)

    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)

    g.add_edge(1, 2, 1)
    g.add_edge(1, 3, 1)
    g.add_edge(2, 4, 1)

    levels = bfs(g, 1)
    
    assert levels[1] == 0  
    assert levels[2] == 1  
    assert levels[3] == 1  
    assert levels[4] == 2  