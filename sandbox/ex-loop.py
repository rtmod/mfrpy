import igraph as ig
import mfrpy as mfr

loopy = ig.Graph(n = 4, edges = [[0,1],[0,2],[1,1],[1,3],[2,3]])
loopy.get_edgelist()

loopy.vs["name"]    = ["A", "B", "C", "D"]
loopy.es["synergy"] = [0, 0, 0, 1, 1]
loopy.es["sign"]    = [1, 1, 1, 1, 1]

mfr.sgmfr.get_mfrs(loopy, [0], 3, verbose = 1)

loopy.es["synergy"] = [1, 0, 1, 2, 2]
mfr.sgmfr.get_mfrs(loopy, [0], 3, verbose = 1)

loopy.es["synergy"] = [0, 0, 0, 1, 1]
mfr.sgmfr.get_mfrs(loopy, [0], 3, verbose = 1)
