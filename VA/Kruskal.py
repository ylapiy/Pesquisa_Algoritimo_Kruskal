class Grafo:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.conexoes = []
        self.nos = [""] * tamanho

    def ConectarNos(self, a, b, peso):
        self.conexoes.append((a, b, peso))

    def nomearNo(self, no, nome):
        if no >= 0 and no < self.tamanho:
            self.nos[no] = nome

    # --- MÉTODOS AUXILIARES DO UNION-FIND (DSU) ---
    def _find(self, pai, i):
        """Busca com compressão de caminho."""
        if pai[i] == i:
            return i
        pai[i] = self._find(pai, pai[i])
        return pai[i]

    def _union(self, pai, altura, x, y):
        """União por rank/altura."""
        raiz_x = self._find(pai, x)
        raiz_y = self._find(pai, y)

        if raiz_x != raiz_y:
            if altura[raiz_x] < altura[raiz_y]:
                pai[raiz_x] = raiz_y
            elif altura[raiz_x] > altura[raiz_y]:
                pai[raiz_y] = raiz_x
            else:
                pai[raiz_y] = raiz_x
                altura[raiz_x] += 1
            return True
        return False

    # --- MÉTODO PRINCIPAL ADAPTADO ---
    def Kruskal(self):
        """
        Retorna a AGM usando a lógica eficiente de conjuntos disjuntos.
        """
        resultado_mst = []

        # 1. Ordenar arestas pelo peso (terceiro elemento da tupla: item[2])
        self.conexoes.sort(key=lambda item: item[2])

        # 2. Inicializar estruturas para o Union-Find
        pai = list(range(self.tamanho))
        altura = [0] * self.tamanho

        # 3. Iterar pelas arestas ordenadas
        for u, v, peso in self.conexoes:
            # Tenta unir os nós. Se retornar True, não havia ciclo.
            if self._union(pai, altura, u, v):
                resultado_mst.append((u, v, peso))

                # Se já pegamos arestas suficientes (V-1), podemos parar
                if len(resultado_mst) == self.tamanho - 1:
                    break

        return resultado_mst

    def PrintarGrafo(self):
        print("Nomes dos nós:", self.nos)
        print("Conexões (u, v, peso):", self.conexoes)
