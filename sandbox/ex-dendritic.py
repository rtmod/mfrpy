import igraph as ig
from sympy.logic.boolalg import to_dnf
from mfrpy import sgmfr

dendrite = ig.Graph.Read_GraphML("sandbox/dendrite.gml")

sgmfr.get_mfrs(dendrite, [32, 36], 29)
sgmfr.get_mfrs(dendrite, [32, 36], 29, verbose = 1)

dendrite = dendrite.simplify(multiple = False, loops = True)

sgmfr.get_mfrs(dendrite, [32], 29)
sgmfr.get_mfrs(dendrite, [36], 29)
sgmfr.get_mfrs(dendrite, [32, 36], 29)
