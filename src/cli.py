import json
import time
import tracemalloc

from graphs.io import carregar_grafo2
from graphs import algorithms


def medir_algoritmo(nome, func, *args):
    """
    Executa um algoritmo medindo tempo e memória.
    Retorna um dicionário formatado.
    """
    tracemalloc.start()
    inicio = time.perf_counter()

    resultado = func(*args)

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
    """
    Executa todos os algoritmos pedidos e gera o arquivo JSON.
    """

    resultados = []

    origem = 1
    destino = 2
    fontes_multisource = [464, 24, 98]

    print("Executando Bellman-Ford...")
    resultados.append(medir_algoritmo(
        "Bellman-Ford",
        algorithms.bellman_ford,
        grafo,
        origem,
        destino
    ))

    print("Executando BFS...")
    resultados.append(medir_algoritmo(
        "BFS",
        algorithms.bfs,
        grafo,
        origem
    ))

    print("Executando DFS...")
    resultados.append(medir_algoritmo(
        "DFS",
        algorithms.dfs,
        grafo,
        origem
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

    #print("\nExecutando Dijkstra...")
    #resultados.append(medir_algoritmo(
    #    "Dijkstra",
    #    algorithms.dijkstra,
     #   grafo,
    #    origem,
    #    destino
    #))

    # Salva o JSON
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


if __name__ == "__main__":
    main()
