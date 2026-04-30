from Kruskal import Grafo
from Desenho import *

a = Grafo(7)

a.nomearNo(0, "A")
a.nomearNo(1, "B")
a.nomearNo(2, "C")
a.nomearNo(3, "D")
a.nomearNo(4, "E")
a.nomearNo(5, "F")
a.nomearNo(6, "G")

a.ConectarNos(0, 1, 4)
a.ConectarNos(0, 6, 10)
a.ConectarNos(0, 2, 9)
a.ConectarNos(1, 2, 8)
a.ConectarNos(2, 3, 5)
a.ConectarNos(2, 4, 2)
a.ConectarNos(2, 6, 7)
a.ConectarNos(3, 4, 3)
a.ConectarNos(3, 5, 7)
a.ConectarNos(4, 6, 6)
a.ConectarNos(5, 6, 11)

a.PrintarGrafo

b = a.Kruskal()
print(b)

desenhar_grafos(a, b)
