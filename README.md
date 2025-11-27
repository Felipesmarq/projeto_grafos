# projeto da disciplina de teoria dos grafos

## Estrutura de arquivos

```shell
  .
  ├── data/                                # Dados que foram usados na parte 1 e 2
      └── relatório                        # Relatório do projeto
  ├── out/                                 # Pasta que contém todas as saidas do projeto(.json/.html/.csv)
      └──html/                             # Pasta com os htmls de visualização do projeto
         ├── arvore_percurso.html
         ├── build_grafo_interativo.py
         ├── grafo_interativo.html
         ├── index.html
         ├── vis_parte2.html
         └── vis_secao8.html
  ├── src/
      ├── graphs/
         ├── graphs.py                     # Classe criada para o Grfo
         ├── io.py                         # Carregar/validar o CSV
         └── algorithms.py                 # BFS, DFS, Dijkstra, Bellman-Ford
      ├── cli.py
      ├── distancias.py                    # Calcular distância PARTE 1
      └── solve.py                         # Arquivo que roda todas as saidas
  ├── README.md
  ├── .gitignore
  └── tests/                               # Tests mínimos e obrigatórios
      ├── test_dijkstra.py
      └── test_bellman_ford.py
      └── test_dfs.py
      └── test_bfs.py
```


## Como gerar saidas do projeto

1. Vá até `projeto_grafos/`
2. Executar `python -m src.solve`

## Como acessar os htmls interativos para visualização do projeto
1. Començando de `projeto_grafos`
2. Executar `cd data/out/html`
3. Por último executar `start .\index.html`

## Requisitos
1. Baixar  `pandas`
2. Abra o prompt de Comando
3. Insira `pip install pandas`
