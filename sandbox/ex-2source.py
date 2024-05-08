import igraph as ig
from sympy.logic.boolalg import to_dnf
from mfrpy import sgmfr

test = ig.Graph(directed = True)
test.add_vertices(6)
test.add_edges([(0,2),(1,3),(1,2),(3,2),(3,4),(3,5),(2,4),(4,5)])
test.vs["name"] = ["i1", "i2", "a", "b", "c", "o"]

sgmfr.get_mfrs(test, [0, 1], 5)
