class Graph:
    def __init__(self):
        self.adj_list = {}
        self.nodes = {}

    def add_node(self, node_name, microrregiao):
        if node_name not in self.adj_list:
            self.adj_list[node_name] = []
            self.nodes[node_name] = {'microrregiao': microrregiao}
            print(f"[Grafo] Nó adicionado: {node_name} (Micro: {microrregiao})")

    def add_edge(self, node1, node2, peso):
        if node1 in self.adj_list and node2 in self.adj_list:
            self.adj_list[node1].append((node2, peso))
            self.adj_list[node2].append((node1, peso))
            print(f"[Grafo] Aresta: {node1} <-> {node2} (Peso: {peso})")
        else:
            print(f"[Erro] Nó {node1} ou {node2} não existe.")

    def get_nodes(self):
        return list(self.nodes.keys())

    def get_node_attributes(self, node_name):
        return self.nodes.get(node_name)

    def get_neighbors(self, node_name):
        return self.adj_list.get(node_name, [])

    def get_order(self):
        return len(self.nodes)

    def get_size(self):
        total_edges = sum(len(neighbors) for neighbors in self.adj_list.values())
        return total_edges // 2
    
    def get_density(self):
        n = self.get_order()
        m = self.get_size()
        if n < 2:
            return 0
        return (2 * m) / (n * (n - 1))
    
    def subgraph_from_nodes(self, nodes_subset):
        """ Retorna um novo grafo apenas com os nós do subset e arestas entre eles """
        sg = Graph()
        for n in nodes_subset:
            meta = self.get_node_attributes(n)
            if meta:
                sg.add_node(n, meta['microrregiao'])

        for n in nodes_subset:
            for (viz, peso) in self.get_neighbors(n):
                if viz in nodes_subset:
                    sg.add_edge(n, viz, peso)

        return sg

    def subgraph_by_microrregiao(self, microrregiao):
        """ Subgrafo induzido por uma microrregião """
        nodes = [n for n, attr in self.nodes.items() if attr['microrregiao'] == microrregiao]
        return self.subgraph_from_nodes(nodes)

    def ego_network(self, node):
        """ Ego network: v ∪ N(v) """
        if node not in self.adj_list:
            return None

        egonodes = {node} | {v for v, _ in self.get_neighbors(node)}
        return self.subgraph_from_nodes(egonodes)

    def degree(self, node):
        return len(self.get_neighbors(node))