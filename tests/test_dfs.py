from graphs.graph import Graph
from graphs.algorithms import dfs

def test_dfs_cycle_and_edge_classification():
    g = Graph(directed=True)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)

    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 1, 1) 
    g.add_edge(2, 4, 1)

    result = dfs(g, 1)

    assert result['has_cycle'] is True
    
    edges = result['edges']
    
    assert ('tree', 1, 2) in edges
    assert ('tree', 2, 3) in edges
    assert ('tree', 2, 4) in edges
    
    assert ('back', 3, 1) in edges