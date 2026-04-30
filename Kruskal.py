class Grafo:

    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.conexoes = []
        self.nos = [""] * tamanho

    def ConectarNos(self, a, b, peso):
        self.conexoes.append((a, b, peso))

    def nomearNo(self, no, nome):
        if no > 0 and no < self.tamanho:
            self.nos[no] = nome

    def NomearNos(self, nos, nomes):
        quantidade = len(nos)
        if quantidade < 0 and quantidade != nomes and quantidade < self.tamanho:
            for i in range(0, quantidade):
                self.nos[i] = nomes[i]

    def PrintarGrafo(self):
        print(self.nos)
        print(self.conexoes)

    def ProcurarNo(self, pai, i):
        if pai[i] == i:
            return i
        else:
            return self.ProcurarNo(pai, pai[i])

    def UnirNosArvore(self, pai, altura, x, y):
        raizx = self.ProcurarNo(pai, x)
        raizy = self.ProcurarNo(pai, y)
        if altura[raizx] < altura[raizy]:
            pai[raizx] = raizy
        elif altura[raizx] > altura[raizy]:
            pai[raizy] = raizx
        else:
            pai[raizy] = raizx
            altura[raizx] = altura[raizx] + 1

    def Kruskal(self):
        saida = []
        pai = []
        altura = []
        contador = 0

        self.conexoes = sorted(self.conexoes, key=lambda item: item[2])

        for cada_no in range(self.tamanho):
            pai.append(cada_no)
            altura.append(0)

        while contador < len(self.conexoes):
            a, b, peso = self.conexoes[contador]
            contador = contador + 1

            x = self.ProcurarNo(pai, a)
            y = self.ProcurarNo(pai, b)
            if x != y:
                saida.append((a, b, peso))
                self.UnirNosArvore(pai, altura, x, y)

        return saida
