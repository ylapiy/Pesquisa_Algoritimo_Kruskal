import networkx as nx
import matplotlib.pyplot as plt


def desenhar_grafos(grafo_original, resultado_kruskal):
    # Criar objetos de Grafo
    G = nx.Graph()
    MST = nx.Graph()

    # Adicionar todos os nós com seus nomes
    for i in range(grafo_original.tamanho):
        nome = grafo_original.nos[i] if grafo_original.nos[i] != "" else str(i)
        G.add_node(i, label=nome)
        MST.add_node(i, label=nome)

    # Adicionar arestas
    for u, v, peso in grafo_original.conexoes:
        G.add_edge(u, v, weight=peso)

    for u, v, peso in resultado_kruskal:
        MST.add_edge(u, v, weight=peso)

    # --- AJUSTE DE LAYOUT PARA MAIS ESPAÇO ---
    # k: distância entre nós (aumente para espalhar mais)
    # iterations: mais iterações deixam o posicionamento mais estável
    pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Configurações de estilo comuns
    estilo_nos = {
        "node_size": 1000,
        "node_color": "#74b9ff",
        "edgecolors": "black",
        "linewidths": 1.5,
        "font_size": 14,
        "font_weight": "bold",
        "with_labels": True,
    }

    # --- 1. Grafo Original ---
    nx.draw(G, pos, ax=ax1, **estilo_nos)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax1,
        edgelist=G.edges(),
        edge_color="blue",
        connectionstyle="angle3,angleA=90, angleB=0",  # Isso cria uma leve curvatura
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax1, font_color="red")
    ax1.set_title("Grafo Original", pad=20, fontsize=16)

    # --- 2. Árvore Geradora Mínima (Kruskal) ---
    # Desenhamos os mesmos nós para manter a referência
    nx.draw(MST, pos, ax=ax2, **estilo_nos)

    # Destacamos as arestas da MST
    labels_mst = nx.get_edge_attributes(MST, "weight")
    nx.draw_networkx_edge_labels(
        MST, pos, edge_labels=labels_mst, ax=ax2, font_color="blue"
    )
    ax2.set_title("Árvore Geradora Mínima (Kruskal)", pad=20, fontsize=16)

    # Remove as bordas dos eixos para ficar limpo
    ax1.axis("off")
    ax2.axis("off")
    plt.tight_layout()
    plt.show()
