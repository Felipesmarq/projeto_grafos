import csv
import json
import math
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # sobe de out/html para raiz
DATA_DIR = BASE_DIR / "data"
OUT_DATA_DIR = BASE_DIR / "out"
OUT_DIR = BASE_DIR / "out" / "html"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# --------- Helpers de leitura --------- #

def load_bairros():
    """
    Espera um CSV com pelo menos uma coluna 'bairro' (ou similar).
    """
    path = DATA_DIR / "bairros_unique.csv"
    bairros = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # tente achar o nome da coluna
        fieldnames = [c.lower() for c in reader.fieldnames]
        if "bairro" in fieldnames:
            col = reader.fieldnames[fieldnames.index("bairro")]
        elif "nome" in fieldnames:
            col = reader.fieldnames[fieldnames.index("nome")]
        else:
            # chuta primeira coluna
            col = reader.fieldnames[0]

        for row in reader:
            nome = row[col].strip()
            if nome:
                bairros.append(nome)
    return bairros


def load_graus(bairros_index):
    path = OUT_DATA_DIR / "graus.csv"
    graus = [0.0] * len(bairros_index)
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fn = [c.lower() for c in reader.fieldnames]
        # tenta casar 'bairro' e 'grau'
        if "bairro" in fn:
            col_bairro = reader.fieldnames[fn.index("bairro")]
        else:
            col_bairro = reader.fieldnames[0]
        if "grau" in fn:
            col_grau = reader.fieldnames[fn.index("grau")]
        else:
            col_grau = reader.fieldnames[1]

        for row in reader:
            nome = row[col_bairro].strip()
            if nome in bairros_index:
                try:
                    graus[bairros_index[nome]] = float(row[col_grau])
                except ValueError:
                    graus[bairros_index[nome]] = 0.0
    return graus


def load_ego(bairros_index):
    path = OUT_DATA_DIR / "ego_bairro.csv"
    dens = [1.0] * len(bairros_index)
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fn = [c.lower() for c in reader.fieldnames]
        if "bairro" in fn:
            col_bairro = reader.fieldnames[fn.index("bairro")]
        else:
            col_bairro = reader.fieldnames[0]
        # densidade / ego_density / algo assim
        cand_cols = [c for c in reader.fieldnames if "dens" in c.lower()]
        if cand_cols:
            col_dens = cand_cols[0]
        else:
            col_dens = reader.fieldnames[1]

        for row in reader:
            nome = row[col_bairro].strip()
            if nome in bairros_index:
                try:
                    dens[bairros_index[nome]] = float(row[col_dens])
                except ValueError:
                    dens[bairros_index[nome]] = 1.0
    return dens


def load_microrregioes(bairros_index):
    """
    Lê a microrregião de cada bairro a partir de bairros_unique.csv.

    Premissa:
      - bairros_unique.csv tem pelo menos:
        - uma coluna com o nome do bairro (ex: 'bairro', 'nome', 'nome_bairro'…)
        - uma coluna com a chave da microrregião (ex: 'microrregiao', 'mic_regiao', etc.)

    O JSON microrregioes.json continua existindo, mas aqui ele NÃO é usado.
    """
    path = DATA_DIR / "bairros_unique.csv"

    if not path.exists():
        # se não tiver o CSV, devolve tudo -1
        return [-1] * len(bairros_index)

    mic = [-1] * len(bairros_index)

    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fn = [c.lower() for c in reader.fieldnames]

        # coluna de bairro
        col_bairro = None
        for original, lower in zip(reader.fieldnames, fn):
            if lower in ("bairro", "bairros", "nome", "nome_bairro"):
                col_bairro = original
                break
        if col_bairro is None:
            # fallback: primeira coluna
            col_bairro = reader.fieldnames[0]

        # coluna de microrregião (ex: 'microrregiao', 'mic_regiao', etc.)
        col_mic = None
        for original, lower in zip(reader.fieldnames, fn):
            if "microrreg" in lower or "mic_reg" in lower or lower == "mic":
                col_mic = original
                break
        if col_mic is None:
            # se não achar nada, chuta segunda coluna
            col_mic = reader.fieldnames[min(1, len(reader.fieldnames) - 1)]

        for row in reader:
            nome = str(row[col_bairro]).strip()
            if not nome:
                continue
            if nome not in bairros_index:
                continue

            raw_val = row[col_mic]
            try:
                val = int(raw_val)
            except (ValueError, TypeError):
                val = -1

            mic[bairros_index[nome]] = val

    return mic


def load_edges(bairros_index):
    """
    adjacencias_bairros.csv – precisa de duas colunas:
    algo tipo 'source'/'target' ou 'origem'/'destino' etc.
    """
    path = DATA_DIR / "adjacencias_bairros.csv"
    edges = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fn = [c.lower() for c in reader.fieldnames]

        # tenta descobrir as duas colunas de bairros
        candidatos = []
        for i, name in enumerate(fn):
            if any(k in name for k in ["origem", "source", "de", "bairro1", "u"]):
                candidatos.append((i, "from"))
            if any(k in name for k in ["dest", "target", "para", "bairro2", "v"]):
                candidatos.append((i, "to"))

        if not candidatos:
            # fallback: assume 2 primeiras colunas
            col_from = reader.fieldnames[0]
            col_to = reader.fieldnames[1]
        else:
            # mapeia
            colnames = reader.fieldnames
            col_from = next(
                (colnames[i] for i, t in candidatos if t == "from"), colnames[0]
            )
            col_to = next(
                (colnames[i] for i, t in candidatos if t == "to"),
                colnames[min(1, len(colnames) - 1)],
            )

        for row in reader:
            a = row[col_from].strip()
            b = row[col_to].strip()
            if a in bairros_index and b in bairros_index and a != b:
                edges.append((bairros_index[a], bairros_index[b]))

    return edges

def _normalize_name(s: str) -> str:
    """
    Normaliza nomes de bairros para comparação:
    - lowercase
    - remove acentos
    - remove pedaço após parênteses (ex: 'Boa Viagem (Setúbal)' -> 'boa viagem')
    - strip espaços extras
    """
    if s is None:
        return ""
    s = s.strip()

    # remove trecho entre parênteses (tipo '(Setúbal)')
    if "(" in s:
        s = s.split("(", 1)[0]

    # lowercase
    s = s.lower().strip()

    # remover acentos
    s_norm = unicodedata.normalize("NFD", s)
    s_norm = "".join(ch for ch in s_norm if not unicodedata.combining(ch))

    # espaço final
    return s_norm.strip()


def load_path_indices(bairros_index):
    """
    Lê o percurso a partir de percurso_nova_descoberta_setubal.json.

    Suporta dois formatos:
    - lista simples de nomes: ["nova descoberta", ..., "boa viagem"]
    - dict com chave "caminho": {"origem": ..., "destino": ..., "caminho": [...]}
    """
    path_file = OUT_DATA_DIR / "percurso_nova_descoberta_setubal.json"
    if not path_file.exists():
        return []

    data = json.loads(path_file.read_text(encoding="utf-8"))

    # Descobre a lista de nomes de bairros
    if isinstance(data, dict) and "caminho" in data:
        nomes_caminho = data["caminho"]
    elif isinstance(data, list):
        nomes_caminho = data
    else:
        nomes_caminho = []

    # mapa nome normalizado -> índice
    norm_map = {_normalize_name(nome): idx for nome, idx in bairros_index.items()}

    indices = []
    for raw in nomes_caminho:
        key = _normalize_name(raw)
        idx = norm_map.get(key)
        if idx is not None:
            indices.append(idx)
        # se não achar, simplesmente ignora o trecho

    return indices


def compute_positions(microrregioes):
    """
    Gera coordenadas (x, y) agrupadas por microrregião.

    - Cada microrregião fica num círculo grande ao redor da origem.
    - Dentro de cada microrregião, os bairros são distribuídos
      em um círculo menor.
    """
    n = len(microrregioes)

    # Agrupa índices por microrregião (mantém -1 como grupo separado)
    clusters = {}
    for idx, mic in enumerate(microrregioes):
        mic_val = mic if mic is not None else -1
        clusters.setdefault(mic_val, []).append(idx)

    # Ordena microrregiões: todas válidas primeiro, depois -1 (sem microrregião)
    ordered_micros = sorted([m for m in clusters.keys() if m != -1])
    if -1 in clusters:
        ordered_micros.append(-1)

    num_clusters = max(len(ordered_micros), 1)

    # Raio do "anel" de clusters e raio interno de cada cluster
    R_cluster = 12.0
    R_inner_base = 3.5

    node_x = [0.0] * n
    node_y = [0.0] * n

    for ci, mic in enumerate(ordered_micros):
        membros = clusters[mic]
        k = len(membros)

        # Ângulo do centro desse cluster no círculo maior
        angle_c = 2 * math.pi * ci / num_clusters
        cx = R_cluster * math.cos(angle_c)
        cy = R_cluster * math.sin(angle_c)

        if mic == 3:
            R_inner = R_inner_base * 1.8
        else:
            R_inner = R_inner_base

        if k == 1:
            # Se só tem um bairro nessa microrregião, joga no centro do cluster
            idx = membros[0]
            node_x[idx] = cx
            node_y[idx] = cy
        else:
            # Distribui os bairros num círculo pequeno ao redor do centro do cluster
            for j, idx in enumerate(membros):
                angle_n = 2 * math.pi * j / k
                node_x[idx] = cx + R_inner * math.cos(angle_n)
                node_y[idx] = cy + R_inner * math.sin(angle_n)

    return node_x, node_y



# --------- Principal --------- #

def main():
    bairros = load_bairros()
    if not bairros:
        raise RuntimeError("Nenhum bairro carregado de bairros_unique.csv")

    bairros_index = {b: i for i, b in enumerate(bairros)}

    graus = load_graus(bairros_index)
    densidade = load_ego(bairros_index)
    microrregioes = load_microrregioes(bairros_index)
    edges = load_edges(bairros_index)
    path_idx = load_path_indices(bairros_index)

    n = len(bairros)

    # Layout agrupado por microrregião
    node_x, node_y = compute_positions(microrregioes)


    # monta edgeX/edgeY com null separando
    edge_x = []
    edge_y = []
    for u, v in edges:
        edge_x.extend([node_x[u], node_x[v], None])
        edge_y.extend([node_y[u], node_y[v], None])

    # arestas apenas do caminho ND → BV
    path_edge_x = []
    path_edge_y = []
    for i in range(len(path_idx) - 1):
        u = path_idx[i]
        v = path_idx[i + 1]
        path_edge_x.extend([node_x[u], node_x[v], None])
        path_edge_y.extend([node_y[u], node_y[v], None])

    # microrregiões únicas
    unique_micros = sorted({m for m in microrregioes if m != -1})
    mic_color_index = {str(m): i for i, m in enumerate(unique_micros)}

    html_path = OUT_DIR / "grafo_interativo.html"
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <title>Grafo Interativo – Bairros do Recife</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      margin: 0;
      padding: 0;
      background: #020617;
      color: #e5e7eb;
    }}
    header {{
      padding: 20px 28px 8px 28px;
      border-bottom: 1px solid #1f2937;
      background: radial-gradient(circle at top left, #0b1120, #020617);
      position: sticky;
      top: 0;
      z-index: 10;
    }}
    h1 {{
      margin: 0;
      font-size: 24px;
      font-weight: 700;
    }}
    .subtitle {{
      margin-top: 4px;
      font-size: 13px;
      color: #9ca3af;
    }}
    main {{
      padding: 18px 28px 24px 28px;
    }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }}
    .toolbar label {{
      font-size: 11px;
      color: #9ca3af;
    }}
    .toolbar input[type="text"] {{
      background: #020617;
      color: #e5e7eb;
      border-radius: 999px;
      border: 1px solid #374151;
      padding: 4px 12px;
      font-size: 12px;
      outline: none;
      min-width: 220px;
    }}
    .toolbar button {{
      border-radius: 999px;
      border: 1px solid #4b5563;
      background: #0f172a;
      color: #e5e7eb;
      font-size: 11px;
      padding: 5px 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .toolbar button span.dot {{
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: #1850ed;
      display: inline-block;
    }}
    .toolbar button.active {{
      border-color: #1850ed;
      box-shadow: 0 0 0 1px rgba(249,115,22,0.4);
    }}
    .pill {{
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid #1f2937;
      background: #020617;
      color: #9ca3af;
    }}
    #graph {{
      width: 100%;
      height: 640px;
    }}
    .legend-mic {{
      margin-top: 6px;
      font-size: 11px;
      color: #9ca3af;
    }}
    .legend-mic span.badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 0 8px;
      border-radius: 999px;
      border: 1px solid #1f2937;
      margin-right: 4px;
      margin-bottom: 4px;
      background: #020617;
    }}
    .legend-mic span.badge-dot {{
      width: 8px;
      height: 8px;
      border-radius: 999px;
      display: inline-block;
    }}
    .meta {{
      margin-top: 10px;
      font-size: 11px;
      color: #9ca3af;
      line-height: 1.5;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Grafo Interativo – Bairros do Recife</h1>
    <div class="subtitle">
      Cada nó é um bairro; as arestas representam interconexões reais por logradouros. Explore graus, microrregiões e o percurso mínimo entre Nova Descoberta e Boa Viagem (Setúbal).
    </div>
  </header>
  <main>
    <div class="toolbar">
      <span class="pill">Apresentação interativa</span>
      <label for="searchInput">Buscar bairro:</label>
      <input id="searchInput" type="text" placeholder="Digite parte do nome do bairro..." />
      <button id="togglePathBtn">
        <span class="dot"></span>
        Realçar caminho Nova Descoberta → Boa Viagem (Setúbal)
      </button>
    </div>
    <div id="graph"></div>
    <div class="legend-mic" id="micLegend"></div>
    <div class="meta">
      • Passe o mouse sobre um bairro para ver grau total de interconexões, microrregião e densidade da ego-subrede.<br/>
      • Use a busca para destacar um bairro específico e seus vizinhos.<br/>
      • Use o botão de destaque para enxergar rapidamente o caminho calculado por Dijkstra entre Nova Descoberta e Boa Viagem (Setúbal).
    </div>
  </main>

<script>
  const bairros = {json.dumps(bairros, ensure_ascii=False)};
  const graus = {json.dumps(graus)};
  const densidadeEgo = {json.dumps(densidade)};
  const microrregioes = {json.dumps(microrregioes)};
  const nodeX = {json.dumps(node_x)};
  const nodeY = {json.dumps(node_y)};
  const edges = {json.dumps(edges)};
  const pathNodeIdx = {json.dumps(path_idx)};
  const pathEdgeX = {json.dumps(path_edge_x)};
  const pathEdgeY = {json.dumps(path_edge_y)};
  const uniqueMicros = {json.dumps(unique_micros)};
  const micColorIndex = {json.dumps(mic_color_index)};

  const palette = [
    "#22c55e", "#0ea5e9", "#eab308", "#a855f7", "#f97316",
    "#ef4444", "#14b8a6", "#3b82f6", "#ec4899", "#84cc16"
  ];

  function colorForMic(mic) {{
    if (mic === -1 || mic === null) return "#9ca3af";
    const idx = micColorIndex[String(mic)] ?? 0;
    return palette[idx % palette.length];
  }}

  function buildFigure(highlightTerm = "", highlightPath = false) {{
    const term = (highlightTerm || "").trim().toUpperCase();

    // mapa de vizinhança
    const vizinhos = {{}};
    for (const [u, v] of edges) {{
      if (!vizinhos[u]) vizinhos[u] = new Set();
      if (!vizinhos[v]) vizinhos[v] = new Set();
      vizinhos[u].add(v);
      vizinhos[v].add(u);
    }}

    let searchIndices = [];
    if (term) {{
      bairros.forEach((b, idx) => {{
        if (b.toUpperCase().includes(term)) {{
          searchIndices.push(idx);
        }}
      }});
    }}

    const neighborSet = new Set();
    for (const idx of searchIndices) {{
      neighborSet.add(idx);
      const neigh = vizinhos[idx] || new Set();
      for (const v of neigh) neighborSet.add(v);
    }}

    const maxDeg = Math.max(...graus);
    const sizes = graus.map(d => 10 + 12 * (d / (maxDeg || 1)));

    const lineWidth = bairros.map((_, idx) => {{
      const inSearch = searchIndices.includes(idx);
      const inNeighbor = neighborSet.has(idx);
      const inPath = highlightPath && pathNodeIdx.includes(idx);
      if (inSearch) return 3.2;
      if (inNeighbor) return 2.4;
      if (inPath) return 2.8;
      return 1.0;
    }});

    const lineColor = bairros.map((_, idx) => {{
      const inSearch = searchIndices.includes(idx);
      const inNeighbor = neighborSet.has(idx);
      const inPath = highlightPath && pathNodeIdx.includes(idx);
      if (inSearch) return "#ffffff";       // destaque principal
      if (inNeighbor) return "#1850ed";     // vizinhos
      if (inPath) return "#ffffff";         // caminho ND-BV
      return "#020617";
    }});

    const nodeTextColor = bairros.map((_, idx) => {{
      const inSearch = searchIndices.includes(idx);
      const inNeighbor = neighborSet.has(idx);
      const inPath = highlightPath && pathNodeIdx.includes(idx);
      if (inSearch) return "#d6d6d6";       // destaque principal
      if (inNeighbor || inPath) return "#ffffff";     // vizinhos
      return "#1f2937";
    }});

    // Arestas: se não há busca, todas cinza.
    // Se há busca, arestas só aparecem fortes se incidentes a nó pesquisado/vizinho.
    const edgeColors = [];
    const edgeWidths = [];
    for (const [u, v] of edges) {{
      const incidentHighlighted =
        (neighborSet.has(u) && neighborSet.has(v)) ||
        (searchIndices.includes(u) || searchIndices.includes(v));
      if (!term) {{
        edgeColors.push("#1f2937");
        edgeWidths.push(1);
      }} else if (incidentHighlighted) {{
        edgeColors.push("#1850ed");
        edgeWidths.push(2.8);
      }} else {{
        edgeColors.push("rgba(31,41,55,0.15)");
        edgeWidths.push(0.5);
      }}
    }}

    const baseEdges = {{
      x: [],
      y: [],
      mode: "lines",
      line: {{ color: "#1f2937", width: 1 }},
      hoverinfo: "none",
      name: "Interconexões"
    }};

    // reconstruir edgeX/edgeY com cores por segmento
    const edgeTraces = [];
    let currentX = [];
    let currentY = [];
    let currentColor = null;
    let currentWidth = null;

    for (let i = 0; i < edges.length; i++) {{
      const [u, v] = edges[i];
      const c = edgeColors[i];
      const w = edgeWidths[i];
      // cada aresta vira um pequeno trace próprio pra termos cor/espessura diferentes
      edgeTraces.push({{
        x: [nodeX[u], nodeX[v]],
        y: [nodeY[u], nodeY[v]],
        mode: "lines",
        line: {{ color: c, width: w }},
        hoverinfo: "none",
        showlegend: false
      }});
    }}

    const pathEdges = {{
      x: pathEdgeX,
      y: pathEdgeY,
      mode: "lines",
      line: {{ color: "#1850ed", width: highlightPath ? 4 : 0 }},
      hoverinfo: "none",
      name: "Percurso ND → BV (Setúbal)",
      showlegend: false
    }};

    const nodes = {{
      x: nodeX,
      y: nodeY,
      mode: "markers+text",
      text: bairros.map(b => b.toUpperCase()),
      textposition: "top center",
      textfont: {{ size: 10, color: nodeTextColor }},
      hovertemplate:
        "<b>%{{text}}</b><br>" +
        "Grau: %{{customdata[0]}}<br>" +
        "Microrregião: %{{customdata[1]}}<br>" +
        "Densidade ego: %{{customdata[2]:.4f}}<extra></extra>",
      customdata: bairros.map((_, i) => [graus[i], microrregioes[i], densidadeEgo[i]]),
      marker: {{
        size: sizes,
        color: microrregioes.map(mic => colorForMic(mic)),
        line: {{
          width: lineWidth,
          color: lineColor
        }}
      }}
    }};

    const layout = {{
      margin: {{ t: 24, r: 16, b: 16, l: 16 }},
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "#020617",
      xaxis: {{
        showgrid: false,
        zeroline: false,
        showticklabels: false
      }},
      yaxis: {{
        showgrid: false,
        zeroline: false,
        showticklabels: false
      }},
      showlegend: false
    }};

    const data = [...edgeTraces, pathEdges, nodes];

    Plotly.newPlot("graph", data, layout, {{ displayModeBar: false }});

    const legend = document.getElementById("micLegend");
    legend.innerHTML = "";
    const used = Array.from(new Set(microrregioes.filter(m => m !== -1))).sort((a,b) => a-b);
    if (used.length === 0) {{
      legend.textContent = "Microrregiões não disponíveis nos dados carregados.";
      return;
    }}
    legend.innerHTML = "Microrregiões (cores dos nós): ";
    used.forEach(mic => {{
      const span = document.createElement("span");
      span.className = "badge";
      const dot = document.createElement("span");
      dot.className = "badge-dot";
      dot.style.backgroundColor = colorForMic(mic);
      span.appendChild(dot);
      const text = document.createTextNode("Mic. " + mic);
      span.appendChild(text);
      legend.appendChild(span);
    }});
  }}

  document.addEventListener("DOMContentLoaded", () => {{
    let highlightPath = false;
    buildFigure("", highlightPath);

    const searchInput = document.getElementById("searchInput");
    const togglePathBtn = document.getElementById("togglePathBtn");

    searchInput.addEventListener("input", (e) => {{
      const term = e.target.value || "";
      buildFigure(term, highlightPath);
    }});

    togglePathBtn.addEventListener("click", () => {{
      highlightPath = !highlightPath;
      if (highlightPath) {{
        togglePathBtn.classList.add("active");
      }} else {{
        togglePathBtn.classList.remove("active");
      }}
      buildFigure(searchInput.value || "", highlightPath);
    }});
  }});
</script>
</body>
</html>
"""

    html_path.write_text(html, encoding="utf-8")
    print(f"HTML gerado em: {html_path}")


if __name__ == "__main__":
    main()