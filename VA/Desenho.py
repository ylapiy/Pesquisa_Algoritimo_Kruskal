import networkx as nx
import matplotlib.pyplot as plt


def desenhar_grafos(grafo_original, resultado_kruskal):
    G = nx.Graph()
    MST = nx.Graph()

    for i in range(grafo_original.tamanho):
        nome = grafo_original.nos[i] if grafo_original.nos[i] != "" else str(i)
        G.add_node(i, label=nome)
        MST.add_node(i, label=nome)

    for u, v, peso in grafo_original.conexoes:
        G.add_edge(u, v, weight=peso)

    for u, v, peso in resultado_kruskal:
        MST.add_edge(u, v, weight=peso)

    pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    estilo_nos = {
        "node_size": 1000,
        "node_color": "#74b9ff",
        "edgecolors": "black",
        "linewidths": 1.5,
        "font_size": 14,
        "font_weight": "bold",
        "with_labels": True,
    }

    nx.draw(G, pos, ax=ax1, **estilo_nos)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax1,
        edgelist=G.edges(),
        edge_color="blue",
        connectionstyle="angle3,angleA=90, angleB=0",
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax1, font_color="red")
    ax1.set_title("Grafo Original", pad=20, fontsize=16)

    nx.draw(MST, pos, ax=ax2, **estilo_nos)

    labels_mst = nx.get_edge_attributes(MST, "weight")
    nx.draw_networkx_edge_labels(
        MST, pos, edge_labels=labels_mst, ax=ax2, font_color="blue"
    )
    ax2.set_title("Árvore Geradora Mínima (Kruskal)", pad=20, fontsize=16)

    ax1.axis("off")
    ax2.axis("off")
    plt.tight_layout()
    plt.show()
