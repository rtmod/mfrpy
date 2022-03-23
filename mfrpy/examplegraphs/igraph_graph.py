from igraph import *

# example graphs from Wang et al. 2013
dag = Graph(directed = True) # directed acyclic graph, no composite nodes
dag.add_vertices(10)
dag.add_edges([
(0,1), (0,2), (0,3), (1,4), (2,5), (1,5), (3,2), (3,6), (4,7),
(5,7), (5,9), (7,9), (6,8), (6,9), (8,9)
])
dag.vs["name"] = ["I", "A", "B", "C", "D", "E", "F", "G", "H", "O"]
dag.composite_nodes = []

dcg = Graph(directed = True) # directed cyclic graph, no composite nodes
dcg.add_vertices(8)
dcg.add_edges([
(0,1), (0,2), (0,3), (3,4), (4,2), (2,5), (1,5), (5,4), (4,6),
(6,5), (5,7), (6,7)
])
dcg.vs["name"] = ["I", "A", "B", "C", "D", "E", "F", "O"]
dcg.composite_nodes = []

exp_dag = Graph(directed = True) # immitates expanded dag graph
exp_dag.add_vertices(12)
# edges (1, 5) & (2, 5) and (5, 9) & (6, 9) in dag have synergy
exp_dag.add_edges([
(0,1), (0,2), (0,3), (1,4), (3,2), (3,6), (4,7), (5,7),
(7,9), (6,8), (8,9), (5, 10), (6, 10), (10, 9), (1, 11), (2, 11), (11, 5)
])
exp_dag.vs["name"] = ["I", "A", "B", "C", "D", "E", "F", "G", "H", "O", "c1",
"c2"]
exp_dag.composite_nodes = [10, 11] # nodes 10 and 11 are composite nodes

exp_dcg = Graph(directed = True) # immitates expanded dcg graph
exp_dcg.add_vertices(10)
# edges (1, 5) & (2, 5) and (0, 2) & (4, 2) in dcg have synergy
exp_dcg.add_edges([
(0,1), (0,3), (3,4), (5,4), (4,6),
(6,5), (5,7), (6,7), (0, 8), (4, 8), (8, 2), (1, 9), (2, 9), (9, 5)
])
exp_dcg.vs["name"] = ["I", "A", "B", "C", "D", "E", "F", "O", "c1", "c2"]
exp_dcg.composite_nodes = [8, 9] # nodes 8 and 9 are composite nodes
