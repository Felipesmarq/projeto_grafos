from .graphs.io import carregar_grafo

def main():
    print("--- Iniciando Projeto de Grafos (Carregamento) ---")

    grafo = carregar_grafo()

    if grafo:
        print("\n--- Verificação do Grafo ---")
        
        ordem = grafo.get_order()
        tamanho = grafo.get_size()
        
        print(f"Ordem do Grafo (Bairros): {ordem}")
        print(f"Tamanho do Grafo (Conexões): {tamanho}")

if __name__ == "__main__":
    main()