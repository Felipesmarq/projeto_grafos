from .graphs.io import carregar_grafo, carregar_grafo2
from .distancias import calcular_distancias
import pandas as pd
from .cli import gerar_relatorio_parte2

def main():
    print("--- Iniciando Projeto de Grafos (Carregamento) ---")

    grafo = carregar_grafo()

    if grafo:
        recife = []
        recife.append({
            "ordem": grafo.get_order(),
            "tamanho": grafo.get_size(),
            "densidade": round(grafo.get_density(), 4),
            "Bairro com maior grau": max(grafo.get_nodes(), key=lambda n: grafo.degree(n)),
            "Maior grau": max(grafo.degree(n) for n in grafo.get_nodes()),
            "Bairro mais denso" : max(grafo.get_nodes(), key=lambda n: grafo.ego_network(n).get_density()),
            "Maior densidade": max(grafo.ego_network(n).get_density() for n in grafo.get_nodes())
            })

    df_recife = pd.DataFrame(recife)
    df_recife.to_json("out/recife.json", orient="records", indent=4)
    

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
    df_micro.to_json("out/microrregioes.json",orient="records", indent=4)

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

    print("\n--- Iniciando Projeto de Grafos (Relatório Parte 2) ---")
    btc_grafo = carregar_grafo2()

    if grafo:
        bitcoin = []
        bitcoin.append({
            "ordem": btc_grafo.get_order(),
            "tamanho": btc_grafo.get_size(),
            "dirigido": btc_grafo.directed,
            "densidade": round(btc_grafo.get_density(), 4)
            })

        df_bitcoin = pd.DataFrame(bitcoin)
        df_bitcoin.to_json("out/bitcoin.json", index=False)

    results = []
    for user in btc_grafo.get_nodes():
        ego = btc_grafo.ego_network(user)
        if ego:
            results.append({
                "user": user,
                "grau": btc_grafo.degree(user),
            })

    df_ego = pd.DataFrame(results)
    df_ego.to_csv("out/user.csv", index=False)
    
    gerar_relatorio_parte2(btc_grafo)


if __name__ == "__main__":
    main()