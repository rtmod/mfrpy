from igraph import *

# example graphs from Wang et al. 2013
dag = Graph(directed = True) # directed acyclic graph, no composite nodes
dag.add_vertices(10)
dag.add_edges([
(0,1), (0,2), (0,3), (1,4), (2,5), (1,5), (3,2), (3,6), (4,7),
(5,7), (5,9), (7,9), (6,8), (6,9), (8,9)
])
dag.vs["name"] = ["i", "a", "b", "c", "d", "e", "f", "g", "h", "o"]
dag.es["synergy"] = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0]
# edges (1, 5) & (2, 5) and (5, 9) & (6, 9) have synergy

dcg = Graph(directed = True) # directed cyclic graph, no composite nodes
dcg.add_vertices(8)
dcg.add_edges([
(0,1), (0,2), (0,3), (3,4), (4,2), (2,5), (1,5), (5,4), (4,6),
(6,5), (5,7), (6,7)
])
dcg.vs["name"] = ["i", "a", "b", "c", "d", "e", "f", "o"]
dcg.es["synergy"] = [0, 1, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0]
# edges (1, 5) & (2, 5) and (0, 2) & (4, 2) have synergy

exp_dag = Graph(directed = True) # immitates expanded dag graph
exp_dag.add_vertices(12)
exp_dag.add_edges([
(0,1), (0,2), (0,3), (1,4), (3,2), (3,6), (4,7), (5,7),
(7,9), (6,8), (8,9), (5,10), (6,10), (10,9), (1,11), (2,11), (11,5)
])
exp_dag.vs["name"] = ["i", "a", "b", "c", "d", "e", "f", "g", "h", "o", "c1",
"c2"]
exp_dag.vs["composite"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
# exp_dag.composite_nodes = [10, 11]
# nodes 10 and 11 are composite nodes

exp_dcg = Graph(directed = True) # immitates expanded dcg graph
exp_dcg.add_vertices(10)
exp_dcg.add_edges([
(0,1), (0,3), (3,4), (5,4), (4,6),
(6,5), (5,7), (6,7), (0,8), (4,8), (8,2), (1,9), (2,9), (9,5)
])
exp_dcg.vs["name"] = ["i", "a", "b", "c", "d", "e", "f", "o", "c1", "c2"]
exp_dag.vs["composite"] = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
# exp_dcg.composite_nodes = [8, 9]
# nodes 8 and 9 are composite nodes

# example graph with a loop
self_loop = Graph(directed = True)
self_loop.add_vertices(5)
self_loop.add_edges(
[(0,1), (0,2), (1,4), (1,3), (2,3), (3,3), (3,4)]
)
self_loop.vs["name"] = ["i", "a", "b", "c", "o"]
self_loop.es["synergy"] = [0, 0, 0, 1, 1, 0, 0]

# example graph from Wang & Albert 2011, modified to include synergy
inhib = Graph(directed = True)
inhib.add_vertices(6)
inhib.add_edges(
[(0,1), (0,2), (0,3), (1,3), (2,3), (3,4), (4,5)]
)
inhib.vs["name"] = ["i", "a", "b", "c", "d", "o"]
inhib.es["synergy"] = [0, 0, 0, 1, 1, 0, 0]
inhib.es["inhibition"] = [0, 0, 1, 1, 1, 1, 0]
# edges (0,3), (1,3), (2,3) & (3,4) are inhibitory edges
