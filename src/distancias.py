import pandas as pd
import json
from .graphs.io import carregar_grafo

def calcular_distancias():
    grafo = carregar_grafo()

    df = pd.read_csv("data/enderecos.csv")

    resultados = []

    for _, row in df.iterrows():
        bairro_x = row["bairro_X"]
        bairro_y = row["bairro_Y"]

        custo, caminho = grafo.dijkstra(bairro_x, bairro_y)

        resultados.append({
            "X": row["X"],
            "Y": row["Y"],
            "bairro_X": bairro_x,
            "bairro_Y": bairro_y,
            "custo": custo,
            "caminho": " -> ".join(caminho)
        })

    pd.DataFrame(resultados).to_csv("data/out/distancias_enderecos.csv", index=False)

    custo, caminho = grafo.dijkstra("nova descoberta", "boa viagem")

    with open("data/out/percurso_nova_descoberta_setubal.json", "w", encoding="utf-8") as f:
        json.dump({
            "origem": "nova descoberta",
            "destino": "setubal (boa viagem)",
            "custo": custo,
            "caminho": caminho
        }, f, indent=4, ensure_ascii=False)

    print("Arquivos gerados com sucesso!")


if __name__ == "__main__":
    calcular_distancias()
