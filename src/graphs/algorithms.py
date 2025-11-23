from collections import deque

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
    from collections import deque

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

