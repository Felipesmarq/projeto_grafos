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


def carregar_grafo2(path_nodes='data/nodes.csv', path_edges='data/bitcoinGraph.csv'):
    
    g = Graph()

    try:
        df_nodes = pd.read_csv(path_nodes)
        
        for _, row in df_nodes.iterrows():
            node_id = row['node_id'] 

            g.add_node(node_name=node_id, microrregiao=None)
            
        print(f"--- Nós carregados: {len(g.nodes)} usuários lidos de '{path_nodes}'")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo de nós não encontrado em '{path_nodes}'")
        return None
    except KeyError:
        print("Erro: O 'nodes.csv' deve ter a coluna 'node_id'.")
        return None

    try:
        df_edges = pd.read_csv(path_edges)
        erros = []

        for idx, row in df_edges.iterrows():
            try:
                peso = float(row['rating']) 
                
                g.add_edge(
                    node1=row['source'],
                    node2=row['target'],
                    peso=peso
                )

            except Exception as e:
                erros.append((idx + 2, row.to_dict(), str(e)))

        num_edges = len(g.adj_list) if hasattr(g, 'adj_list') else "N/A" 
        print(f"--- Arestas processadas de '{path_edges}'")

    except FileNotFoundError:
        print(f"Aviso: Arquivo de arestas '{path_edges}' não encontrado.")
        return None
    except KeyError:
        print("Erro: O CSV de arestas deve ter as colunas 'source', 'target' e 'rating'.")
        return None

    return g