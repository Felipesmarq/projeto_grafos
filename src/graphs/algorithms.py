from collections import deque
import heapq

def dijkstra(grafo, origem, destino):

    dist = {n: float("inf") for n in grafo.nodes}
    dist[origem] = 0

    anterior = {n: None for n in grafo.nodes}
    heap = [(0, origem)]

    while heap:
        atual_dist, atual = heapq.heappop(heap)

        if atual == destino:
            break
        if atual_dist > dist[atual]:
            continue

        for viz, peso in grafo.adj_list[atual]:

            peso_transformado = 10 - peso # invertendo os pesos para aceitar pesos negativos

            novo_custo = atual_dist + peso_transformado

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


def bellman_ford(grafo, origem, destino):

    dist = {n: float("inf") for n in grafo.nodes}
    dist[origem] = 0

    anterior = {n: None for n in grafo.nodes}

    for _ in range(len(grafo.nodes) - 1):
        trocou = False
        
        for atual in grafo.nodes:
            if dist[atual] == float("inf"):
                continue

            for viz, peso in grafo.adj_list[atual]:
                
                novo_custo = dist[atual] + peso 

                if novo_custo < dist[viz]:
                    dist[viz] = novo_custo
                    anterior[viz] = atual
                    trocou = True
        
        if not trocou:
            break

    tem_ciclo_negativo = False
    for atual in grafo.nodes:
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
    visitado = set()
    fila = deque([origem])
    ordem = []

    visitado.add(origem)

    while fila:
        atual = fila.popleft()
        ordem.append(atual)

        for viz in grafo.adj[atual]:
            if viz not in visitado:
                visitado.add(viz)
                fila.append(viz)

    return ordem

def dfs(grafo, origem):
    visitado = set()
    ordem = []

    def explorar(no):
        visitado.add(no)
        ordem.append(no)

        for viz in grafo.adj[no]:
            if viz not in visitado:
                explorar(viz)

    explorar(origem)
    return ordem

# ===============================================================
# BFS a partir de múltiplas fontes (≥ 3)
# Retorna: ordem de visita, camadas, ciclos detectados
# ===============================================================

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

        for viz in grafo.adj[atual]:
            if viz not in visitado:
                visitado.add(viz)
                camada[viz] = camada[atual] + 1
                fila.append(viz)
            else:
                # Detecta ciclo (quando viz já visitado não é o pai direto)
                if camada[viz] <= camada[atual]:
                    ciclos.append((atual, viz))

    return ordem, camada, ciclos


# ===============================================================
# DFS a partir de múltiplas fontes (≥ 3)
# Retorna: ordem, profundidades e ciclos
# ===============================================================

def dfs_multisource(grafo, fontes):
    visitado = set()
    ordem = []
    profundidade = {}
    ciclos = []

    def explorar(no, prof):
        visitado.add(no)
        ordem.append(no)
        profundidade[no] = prof

        for viz in grafo.adj[no]:
            if viz not in visitado:
                explorar(viz, prof + 1)
            else:
                if profundidade[viz] <= profundidade[no] - 1:
                    ciclos.append((no, viz))

    for f in fontes:
        if f not in visitado:
            explorar(f, 0)

    return ordem, profundidade, ciclos

