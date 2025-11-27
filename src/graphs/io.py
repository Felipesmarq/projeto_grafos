import pandas as pd
from .graph import Graph

def carregar_grafo(path_nodes='data/bairros_unique.csv',
                   path_edges='data/adjacencias_bairros.csv'):

    g = Graph(False)

    try:
        df_nodes = pd.read_csv(path_nodes)
        for _, row in df_nodes.iterrows():
            g.add_node(node_name=row['bairro'], microrregiao=row['microrregiao'])
        print(f"--- Nós carregados: {g.get_order()} bairros lidos de '{path_nodes}'")
    except FileNotFoundError:
        print(f"Erro: Arquivo de nós não encontrado em '{path_nodes}'")
        return None
    except KeyError:
        print("Erro: O 'bairros_unique.csv' deve ter as colunas 'bairro' e 'microrregiao'.")
        return None

    try:
        df_edges = pd.read_csv(path_edges)

        erros = []

        for idx, row in df_edges.iterrows():
            try:
                peso = float(row['peso'])
                g.add_edge(
                    node1=row['bairro_origem'],
                    node2=row['bairro_destino'],
                    peso=peso
                )

            except Exception as e:
                erros.append((idx + 2, row.to_dict(), str(e)))


        if erros:
            print("\n⚠ Linhas com erro na coluna 'peso':")
            for linha, dados, erro in erros:
                print(f"\n  → Linha {linha}: {dados}")
                print(f"    Erro: {erro}")

    except FileNotFoundError:
        print(f"Aviso: Arquivo de arestas '{path_edges}' não encontrado.")
    except KeyError:
        print("Erro: O CSV deve ter as colunas 'bairro_origem', 'bairro_destino' e 'peso'.")

    return g


def carregar_grafo2(path_edges='data/bitcoinGraph.csv'):
    
    btc_g = Graph(True)

    try:
        df_edges = pd.read_csv(path_edges)
        erros = []

        for _, row in df_edges.iterrows():
            source = int(row['SOURCE'])
            target = int(row['TARGET'])
            rate = float(row['RATE'])

            if source not in btc_g.nodes:
                btc_g.add_node(source)
            if target not in btc_g.nodes:
                btc_g.add_node(target)

            btc_g.add_edge(source, target, rate)

        num_edges = len(btc_g.adj_list) if hasattr(btc_g, 'adj_list') else "N/A" 
        print(f"--- Arestas processadas de '{path_edges}'")

    except FileNotFoundError:
        print(f"Aviso: Arquivo de arestas '{path_edges}' não encontrado.")
        return None

    return btc_g