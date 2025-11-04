import pandas as pd
from .graph import Graph  

def carregar_grafo(path_nodes='data/bairros_unique.csv', 
                   path_edges='data/adjacencias_bairros.csv'):

    g = Graph()
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
        for _, row in df_edges.iterrows():
            g.add_edge(node1=row['bairro_origem'], 
                       node2=row['bairro_destino'], 
                       peso=row['peso'])
        print(f"--- Arestas carregadas: {g.get_size()} conexões lidas de '{path_edges}'")
    except FileNotFoundError:
        print(f"Aviso: Arquivo de arestas '{path_edges}' não encontrado. O grafo será carregado sem arestas.")
    except KeyError:
        print("Erro: O 'adjacencias_bairros.csv' deve ter as colunas 'bairro_origem', 'bairro_destino' e 'peso'.")

    return g