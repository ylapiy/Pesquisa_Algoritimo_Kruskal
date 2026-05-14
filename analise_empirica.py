"""
Análise Empírica do Algoritmo de Kruskal
=========================================
Coleta tempos de execução para grafos de tamanhos crescentes,
gera gráficos e compara com a curva teórica O(E log E).
"""

import time
import math
import random
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

sys.path.insert(0, ".")
from Kruskal import Grafo


def gerar_grafo_aleatorio(num_nos, densidade=0.5, seed=None):
    """
    Cria um Grafo com 'num_nos' nós e arestas aleatórias.
    densidade controla a proporção de arestas em relação ao máximo possível.
    """
    rng = random.Random(seed)
    g = Grafo(num_nos)
    max_arestas = num_nos * (num_nos - 1) // 2
    num_arestas = max(num_nos - 1, int(max_arestas * densidade))

    arestas_possiveis = [(i, j) for i in range(num_nos) for j in range(i + 1, num_nos)]
    rng.shuffle(arestas_possiveis)

    # Garante conectividade com uma árvore geradora aleatória
    nos_permutados = list(range(num_nos))
    rng.shuffle(nos_permutados)
    for k in range(1, num_nos):
        u = nos_permutados[k - 1]
        v = nos_permutados[k]
        peso = rng.randint(1, 100)
        g.ConectarNos(u, v, peso)

    arestas_ja = {(min(u, v), max(u, v)) for u, v, _ in g.conexoes}
    extras_adicionadas = 0
    for u, v in arestas_possiveis:
        if extras_adicionadas >= num_arestas - (num_nos - 1):
            break
        par = (min(u, v), max(u, v))
        if par not in arestas_ja:
            g.ConectarNos(u, v, rng.randint(1, 100))
            arestas_ja.add(par)
            extras_adicionadas += 1

    return g


# ──────────────────────────────────────────────
# 2. Coleta de tempos
# ──────────────────────────────────────────────


def coletar_tempos(tamanhos_nos, repeticoes=5, densidade=0.5):
    """
    Para cada tamanho de grafo, executa Kruskal 'repeticoes' vezes
    e registra tempo médio e número de arestas.
    """
    resultados = []
    for n in tamanhos_nos:
        tempos = []
        num_arestas = 0
        for r in range(repeticoes):
            g = gerar_grafo_aleatorio(n, densidade=densidade, seed=r * 1000 + n)
            num_arestas = len(g.conexoes)
            inicio = time.perf_counter()
            g.Kruskal()
            fim = time.perf_counter()
            tempos.append(fim - inicio)

        tempo_medio = sum(tempos) / len(tempos)
        resultados.append(
            {
                "nos": n,
                "arestas": num_arestas,
                "tempo_medio_s": tempo_medio,
                "tempo_medio_ms": tempo_medio * 1000,
            }
        )
        print(
            f"  n={n:4d} | arestas={num_arestas:6d} | tempo médio={tempo_medio*1000:.4f} ms"
        )

    return resultados


# ──────────────────────────────────────────────
# 3. Geração dos gráficos
# ──────────────────────────────────────────────


def plotar_resultados(resultados):
    nos = [r["nos"] for r in resultados]
    arestas = [r["arestas"] for r in resultados]
    tempos = [r["tempo_medio_ms"] for r in resultados]

    # Curva teórica normalizada: E * log2(E), escalada para ficar na mesma ordem
    teorico_bruto = [e * math.log2(e) if e > 1 else 0 for e in arestas]
    if max(teorico_bruto) > 0:
        escala = max(tempos) / max(teorico_bruto)
        teorico = [v * escala for v in teorico_bruto]
    else:
        teorico = teorico_bruto

    fig = plt.figure(figsize=(16, 12))
    fig.suptitle(
        "Análise Empírica — Algoritmo de Kruskal",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.40, wspace=0.35)

    # ── Gráfico 1: Tempo (ms) × Nº de Nós ──────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(
        nos, tempos, marker="o", color="#2980b9", linewidth=2, label="Tempo medido"
    )
    ax1.set_title("Tempo de Execução × Nº de Nós")
    ax1.set_xlabel("Número de Nós")
    ax1.set_ylabel("Tempo médio (ms)")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.5)

    # ── Gráfico 2: Tempo (ms) × Nº de Arestas ──────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(
        arestas, tempos, marker="s", color="#27ae60", linewidth=2, label="Tempo medido"
    )
    ax2.set_title("Tempo de Execução × Nº de Arestas")
    ax2.set_xlabel("Número de Arestas (E)")
    ax2.set_ylabel("Tempo médio (ms)")
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.5)

    # ── Gráfico 3: Comparação empírico × teórico O(E log E) ─────────────
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(
        arestas, tempos, marker="o", color="#2980b9", linewidth=2, label="Empírico"
    )
    ax3.plot(
        arestas,
        teorico,
        marker="^",
        color="#e74c3c",
        linewidth=2,
        linestyle="--",
        label="Teórico O(E·log E) — normalizado",
    )
    ax3.set_title("Empírico vs. Teórico O(E·log E)")
    ax3.set_xlabel("Número de Arestas (E)")
    ax3.set_ylabel("Tempo (ms) / Valor normalizado")
    ax3.legend()
    ax3.grid(True, linestyle="--", alpha=0.5)

    # ── Gráfico 4: Escala log-log para confirmar complexidade ────────────
    ax4 = fig.add_subplot(gs[1, 1])
    log_arestas = [math.log10(e) for e in arestas if e > 0]
    log_tempos = [math.log10(t) if t > 0 else 0 for t in tempos]
    ax4.plot(
        log_arestas,
        log_tempos,
        marker="D",
        color="#8e44ad",
        linewidth=2,
        label="log(tempo) × log(arestas)",
    )
    # Linha de referência com inclinação 1 (linear em log = O(E))
    x_arr = np.array(log_arestas)
    y_ref = x_arr - x_arr[0] + log_tempos[0]
    ax4.plot(
        x_arr, y_ref, linestyle=":", color="gray", label="Referência incl. 1 (linear)"
    )
    ax4.set_title("Escala Log-Log")
    ax4.set_xlabel("log₁₀(Arestas)")
    ax4.set_ylabel("log₁₀(Tempo ms)")
    ax4.legend()
    ax4.grid(True, linestyle="--", alpha=0.5)

    plt.savefig("analise_empirica_kruskal.png", dpi=150, bbox_inches="tight")
    print("\nGráfico salvo em: analise_empirica_kruskal.png")
    plt.show()


# ──────────────────────────────────────────────
# 4. Execução principal
# ──────────────────────────────────────────────

if __name__ == "__main__":
    TAMANHOS = [10, 25, 50, 100, 200, 400, 600, 800, 1000]
    REPETICOES = 7
    DENSIDADE = 0.4

    print("=" * 55)
    print("  Análise Empírica — Algoritmo de Kruskal")
    print("=" * 55)
    print(f"  Tamanhos testados : {TAMANHOS}")
    print(f"  Repetições        : {REPETICOES}")
    print(f"  Densidade de arst.: {DENSIDADE*100:.0f}%")
    print("-" * 55)

    resultados = coletar_tempos(TAMANHOS, repeticoes=REPETICOES, densidade=DENSIDADE)

    print("\n{'Nós':>6} | {'Arestas':>8} | {'Tempo médio (ms)':>18}")
    print("-" * 40)
    for r in resultados:
        print(f"{r['nos']:>6} | {r['arestas']:>8} | {r['tempo_medio_ms']:>18.4f}")

    plotar_resultados(resultados)
