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