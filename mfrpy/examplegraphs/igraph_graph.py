from igraph import Graph, plot

# example graphs from Wang et al. 2013
dag = Graph(directed = True) # directed acyclic graph, no composite nodes
dag.add_vertices(10)
dag.add_edges([
    (0,1), (0,2), (0,3), (1,4),
    (2,5), (1,5), (3,2), (3,6),
    (4,7), (5,7), (5,9), (7,9),
    (6,8), (6,9), (8,9)
    ])
dag.vs["name"] = [
    "i", "a", "b", "c", "d",
    "e", "f", "g", "h", "o"
    ]
dag.es["synergy"] = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0]
# edges (1, 5) & (2, 5) and (5, 9) & (6, 9) have synergy

dcg = Graph(directed = True) # directed cyclic graph, no composite nodes
dcg.add_vertices(8)
dcg.add_edges([
    (0,1), (0,2), (0,3), (3,4),
    (4,2), (2,5), (1,5), (5,4),
    (4,6), (6,5), (5,7), (6,7)
    ])
dcg.vs["name"] = ["i", "a", "b", "c", "d", "e", "f", "o"]
dcg.es["synergy"] = [0, 1, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0]
# edges (1, 5) & (2, 5) and (0, 2) & (4, 2) have synergy

exp_dag = Graph(directed = True) # immitates expanded dag graph
exp_dag.add_vertices(12)
exp_dag.add_edges([
    (0,1), (0,2), (0,3), (1,4),
    (3,2), (3,6), (4,7), (5,7),
    (7,9), (6,8), (8,9), (5,10),
    (6,10), (10,9), (1,11), (2,11),
    (11,5)
    ])
exp_dag.vs["name"] = [
    "i", "a", "b", "c", "d", "e",
    "f", "g", "h", "o", "c1","c2"
    ]
exp_dag.vs["composite"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
# exp_dag.composite_nodes = [10, 11]
# nodes 10 and 11 are composite nodes

exp_dcg = Graph(directed = True) # immitates expanded dcg graph
exp_dcg.add_vertices(10)
exp_dcg.add_edges([
    (0,1), (0,3), (3,4), (5,4),
    (4,6), (6,5), (5,7), (6,7),
    (0,8), (4,8), (8,2), (1,9),
    (2,9), (9,5)
    ])
exp_dcg.vs["name"] = [
    "i", "a", "b", "c", "d",
    "e", "f", "o", "c1", "c2"
    ]
exp_dcg.vs["composite"] = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
# exp_dcg.composite_nodes = [8, 9]
# nodes 8 and 9 are composite nodes

# example graph with a loop
self_loop = Graph(directed = True)
self_loop.add_vertices(5)
self_loop.add_edges([
    (0,1), (0,2), (1,4), (1,3),
    (2,3), (3,3), (3,4)
    ])
self_loop.vs["name"] = ["i", "a", "b", "c", "o"]
self_loop.es["synergy"] = [0, 0, 0, 1, 1, 0, 0]

# example graph from Wang & Albert 2011, modified to include synergy
inhib = Graph(directed = True)
inhib.add_vertices(6)
inhib.add_edges([
    (0,1), (0,2), (0,3), (1,3),
    (2,3), (3,4), (4,5)
    ])
inhib.vs["name"] = ["i", "a", "b", "c", "d", "o"]
inhib.es["synergy"] = [0, 0, 0, 1, 1, 0, 0]
inhib.es["inhibition"] = [0, 0, 1, 1, 1, 1, 0]
# edges (0,3), (1,3), (2,3) & (3,4) are inhibitory edges

# example for testing redundancy in sgmfr i.e. nodes that cannot be activated
impossible = Graph(directed = True)
impossible.add_vertices(5)
impossible.add_edges([
    (0,2), (1,2), (2,4), (3,4)
    ])
impossible.vs["name"] = ["a", "b", "c", "d", "e"]
impossible.es["synergy"] = [1, 1, 2, 2]
impossible.es["inhibition"] = [0, 1, 1, 0]

# Bordetellae immune response graph from Thakar et al
bordetellae = Graph.Read_GraphML("data/bordetellaeGraph.xml")
bordetellae.vs["name"] = bordetellae.vs["id"]
bordetellae.vs["label"] = bordetellae.vs["name"]

# example graph with multiple edges that are part of distinct synergies
manysyns = Graph(directed = True)
manysyns.add_vertices(5)
manysyns.add_edges([
    (0,1), (0,2), (0,3), (1,4),
    (2,4), (2,4), (3,4)
    ])
manysyns.vs["name"] = ["a", "b", "c", "d", "e"]
manysyns.es["synergy"] = [0, 0, 0, 1, 1, 2, 2]


alchemy = Graph(directed = True)
alchemy.add_vertices(7)
alchemy.add_edges([
    (0,1), (0,2), (1,3), (2,3),
    (1,4), (3,4), (3,5), (3,6), (4,6), (5,6),
    ])
alchemy.vs["name"] = [
    "i", "a", "b", "c", "d", "e",
     "o"
    ]
alchemy.es["synergy"] = [0, 0, 1, 1, 2, 2, 0, 0, 0]
alchemy.es["inhibition"] = [0, 0, 0, 1, 0, 0, 0, 0, 0]
alchemy.vs["label"] = alchemy.vs["name"]

alchemy.es.select(2, 3)["color"] = "red"
alchemy.es.select(8, 9)["color"] = "blue"
#plot(alchemy, vertex_label_size = 8, vertex_size = (50), edge_arrow_size = 0.5, vertex_frame_color="white",
     #vertex_color = "white", bbox=(0, 0, 400, 400))

xiao_wnt5a = Graph(directed = True)
xiao_wnt5a.add_vertices(7)
xiao_wnt5a.add_edges([(1,2),(0,2), (1,2),(2,2), (0,2),(2,2), (4,3), (0,1), (3,1), (4,4),
(2,4), (1,5), (4,6), (2,6)])
xiao_wnt5a.vs["name"]=["RET1","HADHB","pirin","S100P","STC2","WNT5A","MART1"]
xiao_wnt5a.es["synergy"] = [1,1,2,2,3,3,0,0,0,0,0,0,0,0]

xiao_wnt5a_simple = Graph(directed = True)
xiao_wnt5a_simple.add_vertices(6)
xiao_wnt5a_simple.add_edges([(0,1),(0,2),(1,2),(0,2),(1,2),(2,4),(4,3),(3,1),(1,5)])
xiao_wnt5a_simple.vs["name"]=["x4","x6","x2","x3","x7","x1"]
xiao_wnt5a_simple.es["synergy"] = [0,0,0,1,1,0,0,0,0]

xiao = Graph(directed = True)
xiao.add_vertices(7)
xiao.add_edges([(0,1),(0,2),(1,2),(0,2),(1,2),(2,4),(4,3),(3,1),(1,5),(2,6),(4,6)])
xiao.vs["name"]=["x4","x6","x2","x3","x7","x1","x5"]
xiao.es["synergy"] = [0,0,0,1,1,0,0,0,0,0,0]

yeast = Graph(directed = True)
yeast.add_vertices(10)
yeast.add_edges([(4,1),(2,1), (2,1), (4,1), (8,2),(7,2),(5,2), (9,3),(8,3),(7,3),(5,3),(1,3),
(7,4), (6,5),(4,5),(3,5), (6,5),(4,5),(2,5), (6,5),(2,5),(3,5), (6,5),(4,5),(2,5),(3,5),
  (4,5),(2,5),(3,5), (0,6), (3,7), (6,8),(4,8),(3,8), (6,8),(4,8),(2,8), (6,8),(2,8),(3,8),
  (4,8),(2,8),(3,8), (6,8),(4,8),(2,8),(3,8), (4,9), (2,9), (4,9),(2,9)])
yeast.es["synergy"] = [1,1, 0, 0, 2,2,2, 3,3,3,3,3, 0, 4,4,4, 5,5,5, 6,6,6, 7,7,7,7, 8,8,8, 0, 0, 9,9,9, 10,10,10, 11,11,11, 12,12,12, 13,13,13,13, 0, 0, 14,14]
yeast.vs["name"]=['Start', 'Cdc25', 'Cdc2_Cdc13', 'Cdc2_Cdc13_A', 'PP', 'Rum1', 'SK', 'Slp1', 'Ste9', 'Wee1_Mik1']
yeast.vs["label"] = yeast.vs["name"]
table = [['Start', 'Cdc25', 'Cdc2_Cdc13', 'Cdc2_Cdc13_A', 'PP', 'Rum1', 'SK', 'Slp1', 'Ste9', 'Wee1_Mik1'],['','(PP&Cdc2_Cdc13)|PP|Cdc2_Cdc13','(Ste9&Slp1&Rum1)','(Wee1_Mik1&Ste9&Slp1&Rum1&Cdc25)', 'Slp1', '(SK&PP&Cdc2_Cdc13_A)|(SK&PP&Cdc2_Cdc13)|(SK&Cdc2_Cdc13_A&Cdc2_Cdc13)|(SK&PP&Cdc2_Cdc13_A&Cdc2_Cdc13)|(PP&Cdc2_Cdc13_A&Cdc2_Cdc13)', 'Start', 'Cdc2_Cdc13_A', '(SK&PP&Cdc2_Cdc13_A)|(SK&PP&Cdc2_Cdc13)|(SK&Cdc2_Cdc13_A&Cdc2_Cdc13)|(PP&Cdc2_Cdc13_A&Cdc2_Cdc13)|(SK&PP&Cdc2_Cdc13_A&Cdc2_Cdc13)', 'PP|Cdc2_Cdc13|(PP&Cdc2_Cdc13)']]
