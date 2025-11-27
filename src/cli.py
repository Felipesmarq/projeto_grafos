import json
import time
import tracemalloc

from .graphs.io import carregar_grafo2
from .graphs import algorithms


def medir_algoritmo(nome, func, *args, **kwargs):

    tracemalloc.start()
    inicio = time.perf_counter()

    resultado = func(*args, **kwargs)

    fim = time.perf_counter()
    tempo = fim - inicio

    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algoritmo": nome,
        "tempo_segundos": tempo,
        "memoria_atual_bytes": memoria_atual,
        "memoria_pico_bytes": memoria_pico,
        "resultado": str(resultado)
    }


def gerar_relatorio_parte2(grafo):

    resultados = []

    origem = [2,3,7, 9, 13,]
    destino = [17,19,23, 29, 31,]
    fontes_multisource = [464, 24, 98]

    for i in range(len(origem)):
        print(f"\nExecutando Dijkstra {i+1}...")
        resultados.append(medir_algoritmo(
            f"Dijkstra {i+1}",
            algorithms.dijkstra,
            grafo,
            origem[i],
            destino[i],
            normalized=True
        ))

    print("Executando Bellman-Ford sem ciclo...")
    resultados.append(medir_algoritmo(
        "Bellman-Ford sem ciclo negativo",
        algorithms.bellman_ford,
        grafo,
        origem[1],
        destino[1],
        normalized=True
    ))

    print("Executando Bellman-Ford com ciclo...")
    resultados.append(medir_algoritmo(
        "Bellman-Ford com ciclo negativo",
        algorithms.bellman_ford,
        grafo,
        origem[3],
        destino[3],
        normalized=False
    ))
    for i in range(3):
        print(f"Executando BFS {i+1}...")
        resultados.append(medir_algoritmo(
            f"BFS {i+1}",
            algorithms.bfs,
            grafo,
            origem[i]
        ))
    for i in range(3):
        print(f"Executando DFS {i+1}...")
        resultados.append(medir_algoritmo(
            f"DFS {i+1}",
            algorithms.dfs,
            grafo,
            origem[i]
        ))

    print("Executando BFS Multisource...")
    resultados.append(medir_algoritmo(
        "BFS Multisource",
        algorithms.bfs_multisource,
        grafo,
        fontes_multisource
    ))

    print("Executando DFS Multisource...")
    resultados.append(medir_algoritmo(
        "DFS Multisource",
        algorithms.dfs_multisource,
        grafo,
        fontes_multisource
    ))

    with open("out/parte2_report.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4)

    print("\n✅ Relatório salvo em: out/parte2_report.json\n")


def main():
    print("Carregando grafo...")
    grafo = carregar_grafo2()

    if not grafo:
        print("Erro: o grafo não foi carregado!")
        return

    gerar_relatorio_parte2(grafo)
