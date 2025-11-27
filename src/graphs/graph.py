import heapq

class Graph:
    def __init__(self, directed):
        self.adj_list = {}
        self.nodes = {}
        self.directed = directed

    def add_node(self, node_name, microrregiao=None):
        if node_name not in self.adj_list:
            self.adj_list[node_name] = []
            self.nodes[node_name] = {'microrregiao': microrregiao}

    def add_edge(self, node1, node2, peso):

        if node1 not in self.adj_list:
            self.add_node(node1)
        if node2 not in self.adj_list:
            self.add_node(node2)

        self.adj_list[node1].append((node2, peso))

        if not self.directed:
            self.adj_list[node2].append((node1, peso))

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
        if self.directed:
            return total_edges
        return total_edges // 2
    
    def get_density(self):
        n = self.get_order()
        m = self.get_size()
        if n < 2:
            return 0
        if self.directed:
            return m / (n * (n - 1))
        return (2 * m) / (n * (n - 1))
    
    def subgraph_from_nodes(self, nodes_subset):
        """ Retorna um novo grafo apenas com os nós do subset e arestas entre eles """
        sg = Graph(directed=self.directed)
        
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
    
    def dijkstra(self, origem, destino):

        dist = {n: float("inf") for n in self.nodes}
        dist[origem] = 0

        anterior = {n: None for n in self.nodes}

        heap = [(0, origem)]

        while heap:
            atual_dist, atual = heapq.heappop(heap)

            if atual == destino:
                break

            if atual_dist > dist[atual]:
                continue

            for viz, peso in self.adj_list[atual]:
                novo_custo = atual_dist + peso

                if novo_custo < dist[viz]:
                    dist[viz] = novo_custo
                    anterior[viz] = atual
                    heapq.heappush(heap, (novo_custo, viz))

        caminho = []
        node = destino
        while node is not None:
            caminho.append(node)
            node = anterior[node]

        caminho.reverse()

        return dist[destino], caminho