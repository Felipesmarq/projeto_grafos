from .graphs.io import carregar_grafo, carregar_grafo2
from .distancias import calcular_distancias
import pandas as pd

def main():
    print("--- Iniciando Projeto de Grafos (Carregamento) ---")

    grafo = carregar_grafo()

    if grafo:
        recife = []
        recife.append({
            "ordem": grafo.get_order(),
            "tamanho": grafo.get_size(),
            "densidade": round(grafo.get_density(), 4)
            })

    df_recife = pd.DataFrame(recife)
    df_recife.to_json("out/recife.json", index=False)
    

    micros = set(attr['microrregiao'] for attr in grafo.nodes.values())

    micro_results = []
    for micro in micros:
        sg = grafo.subgraph_by_microrregiao(micro)
        micro_results.append({
            "microrregiao": micro,
            "ordem": sg.get_order(),
            "tamanho": sg.get_size(),
            "densidade": round(sg.get_density(), 4)
        })

    df_micro = pd.DataFrame(micro_results)
    df_micro.to_json("out/microrregioes.json", index=False)

    ego_results = []
    for bairro in grafo.get_nodes():
        ego = grafo.ego_network(bairro)
        if ego:
            ego_results.append({
                "bairro": bairro,
                "grau": grafo.degree(bairro),
                "ordem_ego": ego.get_order(),
                "tamanho_ego": ego.get_size(),
                "densidade_ego": round(ego.get_density(), 4)
            })

    df_ego = pd.DataFrame(ego_results)
    df_ego.to_csv("out/ego_bairro.csv", index=False)

    graus = [{"bairro": n, "grau": grafo.degree(n)} for n in grafo.get_nodes()]
    df_graus = pd.DataFrame(graus)
    df_graus.to_csv("out/graus.csv", index=False)

    calcular_distancias(grafo)

    btc_grafo = carregar_grafo2()

if __name__ == "__main__":
    main()