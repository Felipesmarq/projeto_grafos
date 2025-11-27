from collections import deque
import heapq

def dijkstra(grafo, origem, destino, normalized=False):
    dist = {n: float("inf") for n in grafo.get_nodes()}
    dist[origem] = 0

    anterior = {n: None for n in grafo.get_nodes()}
    heap = [(0, origem)]

    while heap:
        atual_dist, atual = heapq.heappop(heap)

        if atual == destino:
            break
        if atual_dist > dist[atual]:
            continue

        for viz, peso in grafo.adj_list.get(atual, []):
            if peso < 0 and not normalized:
                raise ValueError("Dijkstra não aceita arestas com peso negativo.")
            if normalized:
                peso = 10 - peso
            novo_custo = atual_dist + peso

            if novo_custo < dist[viz]:
                dist[viz] = novo_custo
                anterior[viz] = atual
                heapq.heappush(heap, (novo_custo, viz))

    if dist[destino] == float("inf"):
        return float("inf"), []

    caminho = []
    node = destino
    while node is not None:
        caminho.append(node)
        node = anterior[node]

    caminho.reverse()

    return dist[destino], caminho


def bellman_ford(grafo, origem, destino, normalized=False):

    dist = {n: float("inf") for n in grafo.get_nodes()}
    dist[origem] = 0

    anterior = {n: None for n in grafo.get_nodes()}

    if normalized:
        tem_ciclo_negativo = False
    else:
        tem_ciclo_negativo = False
        for atual in grafo.get_nodes():
            if dist[atual] == float("inf"):
                continue
            for viz, peso in grafo.adj_list[atual]:
                if dist[atual] + peso < dist[viz]:
                    tem_ciclo_negativo = True
                    break
            if tem_ciclo_negativo:
                break

        if tem_ciclo_negativo:
            print("Erro: Ciclo negativo detectado!")
            return float("-inf"), []

    for _ in range(len(grafo.get_nodes()) - 1):
        trocou = False
        
        for atual in grafo.get_nodes():
            if dist[atual] == float("inf"):
                continue

            for viz, peso in grafo.adj_list[atual]:
                if normalized:
                    peso = 10 - peso
                novo_custo = dist[atual] + peso

                if novo_custo < dist[viz]:
                    dist[viz] = novo_custo
                    anterior[viz] = atual
                    trocou = True
        
        if not trocou:
            break

    caminho = []
    node = destino
    
    if dist[destino] == float("inf"):
        return float("inf"), [] # Destino inalcançável

    while node is not None:
        caminho.append(node)
        node = anterior[node]

    caminho.reverse()

    return dist[destino], caminho


def bfs(grafo, origem):
    levels = {}
    levels[origem] = 0
    
    fila = deque([origem])

    while fila:
        atual = fila.popleft()

        for viz, _ in grafo.adj_list.get(atual, []):
            if viz not in levels:
                levels[viz] = levels[atual] + 1
                fila.append(viz)
                
    return levels

def dfs(grafo, origem):
    visited = set()
    recursion_stack = set()
    
    classified_edges = []
    has_cycle = False
    
    def dfs_visit(u):
        nonlocal has_cycle
        
        visited.add(u)
        recursion_stack.add(u)
        
        for v, _ in grafo.adj_list.get(u, []):
            if v not in visited:
                classified_edges.append(('tree', u, v))
                dfs_visit(v)
            elif v in recursion_stack:
                classified_edges.append(('back', u, v))
                has_cycle = True
            else:
                classified_edges.append(('forward/cross', u, v))
        recursion_stack.remove(u)
    nodes = grafo.get_nodes()
    if origem in nodes:
        dfs_visit(origem)
            
    return {
        'edges': classified_edges,
        'has_cycle': has_cycle
    }


def bfs_multisource(grafo, fontes):

    visitado = set()
    fila = deque()
    camada = {}
    ordem = []
    ciclos = []

    for f in fontes:
        fila.append(f)
        visitado.add(f)
        camada[f] = 0

    while fila:
        atual = fila.popleft()
        ordem.append(atual)

        for viz, _ in grafo.adj_list[atual]:
            if viz not in visitado:
                visitado.add(viz)
                camada[viz] = camada[atual] + 1
                fila.append(viz)
            else:
                if camada[viz] <= camada[atual]:
                    ciclos.append((atual, viz))

    return ordem, camada, ciclos


def dfs_multisource(grafo, fontes):
    visitado = set()
    ordem = []
    profundidade = {}
    ciclos = []

    def explorar(no, prof):
        visitado.add(no)
        ordem.append(no)
        profundidade[no] = prof

        for viz, _ in grafo.adj_list[no]:
            if viz not in visitado:
                explorar(viz, prof + 1)
            else:
                if profundidade[viz] <= profundidade[no] - 1:
                    ciclos.append((no, viz))

    for f in fontes:
        if f not in visitado:
            explorar(f, 0)

    return ordem, profundidade, ciclos