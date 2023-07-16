from igraph import Graph, GraphBase
from mfrpy import update_expand

# bnet in list form
list = ["AKT",           "(NCOR2&PIP3)",
"ALOX15",        "(CREB&STAT3_b1&STAT6)",
"AP1",           "(FOS&JUN)",
"ATF1",          "STAT6",
"AhR",           "(IRF4&STAT6&USF1&NCOR2)|(IRF4&STAT6&USF1&ERK)|(IRF4&STAT6&USF1&NCOR2&ERK)|(IRF4&STAT6&USF1&NCOR2)",
"BATF3",         "(IRF8&USF1)|IRF8",
"BCL2",          "(STAT3_b1&STAT3_b2&JNK)",
"BECN1",         "(STAT3_b1&JNK&BCL2)",
"CCDC151",       "(AP1&CEBPb&PU1_b1)",
"CCL2",          "(FOXO1&STAT3_b1&STAT5&ERK)",
"CCL22",         "(AhR&KLF4&MAFB)|(AhR&FOXO1&KLF4&MAFB)|(AhR&FOXO1&KLF4&NCOR2)|(AhR&FOXO1&KLF4&MAFB&NCOR2)|(AhR&FOXO1&KLF4&MAFB)",
"CD14",          "(FOXO1&KLF4&STAT3_b1&STAT5)",
"CD141",         "(ATF1&CEBPa&CREB&IRF4&USF1)|(ATF1&CEBPa&IRF4&USF1)",
"CD163",         "(IRF8&MAFB&PRDM1)",
"CD1A",          "(BATF3&CEBPa&CEBPb&CREB&IRF4&PRDM1&PU1_b1&NCOR2)|(BATF3&CEBPa&CEBPb&IRF4&PRDM1&PU1_b1&NCOR2)|(BATF3&CEBPa&IRF4&PRDM1&PU1_b1&NCOR2)|(BATF3&IRF4&PRDM1&PU1_b1&NCOR2)",
"CD1B",          "(CEBPa&CEBPb&IRF4&PRDM1)|(CEBPa&CEBPb&PRDM1)|(CEBPa&PRDM1)",
"CD1C",          "(FOXO1&IRF4&NR4A1&PU1_b1&STAT6)",
"CD206",         "(IRF8&MAFB&PRDM1&USF1)",
"CD209",         "(AP1&CREB&ELK4&IRF4&PU1_b1&STAT6)",
"CD226",         "(BATF3&CEBPa&FOXO1&IRF4&PRDM1&PU1_b1&STAT3_b1&STAT5&STAT6&USF1)|(BATF3&FOXO1&IRF4&PRDM1&PU1_b1&STAT3_b1&STAT5&STAT6&USF1)",
"CD40",          "AP1",
"CD48",          "(IRF4&PU1_b1&PU1_b2)",
"CD83",          "(IRF4&NFKB2&STAT6)",
"CD86",          "AP1",
"CEBPa",         "(FOXO1&IRF8&PU1_b1&STAT5)",
"CEBPb",         "(CEBPa&MAFB&PU1_b1)|(CEBPa&PU1_b1)",
"CIITA",         "STAT5",
"CLIP1",         "(PU1_b1&mTORC1)|PU1_b1",
"CPLA2",         "ERK",
"CREB",          "(AKT&ERK)|AKT",
"CSF2",          "",
"CSF2R",         "CSF2",
"DCIR",          "(PU1_b1&PU1_b2&STAT6)",
"DEC205",        "(AP1&FOXO1&PRDM1)",
"DUOX1",         "(IRF4&PU1_b1&PU1_b2&STAT6)",
"DUSP6",         "ERK",
"ELK4",          "ERK",
"ERK",           "MEK1",
"FLT3",          "PU1_b1",
"FOS",           "ERK",
"FOXO1",         "(KLF4&PU1_b1&AKT)|(KLF4&AKT)",
"GSK3B",         "AKT",
"HLA_DR",        "(STAT3_b1&STAT6&CIITA)|STAT3_b1",
"IKK",           "(CSF2R&AKT)|CSF2R",
"IL4",           "",
"IL4R",          "IL4",
"IL4_gene",      "STAT6",
"IRF4",          "(AhR&NFKB1_RelA&PU1_b1&PU1_b2&STAT6)|AhR",
"IRF8",          "(KLF4&PU1_b1&NCOR2)|(KLF4&NCOR2)",
"ITGAX",         "(IRF4&PRDM1&PU1_b1)",
"JAK1",          "IL4R",
"JAK2",          "(CSF2R&PTPN1)",
"JAK3",          "IL4R",
"JNK",           "ERK",
"JUN",           "JNK",
"KLF4",          "(AP1&PU1_b1&STAT5)|(AP1&IRF8&PU1_b1&STAT5)|(AP1&IRF8&NR4A1&PU1_b1&STAT5)|(AP1&IRF8&NR4A1)",
"LnC_DC",        "(IRF4&PU1_b1&STAT5)",
"MAFB",          "(AhR&CEBPb&IRF8&PU1_b1)|(AhR&CEBPb&IRF8&PU1_b1&PU1_b2)|(AhR&CEBPb&PU1_b1)|(AhR&CEBPb&PU1_b1&PU1_b2)",
"MAGI1",         "MEK1",
"MAOA",          "(PU1_b1&PU1_b2&STAT6&NCOR2)",
"MEK1",          "RAF",
"MERTK",         "(IRF8&MAFB)",
"NCOR2",         "(AhR&IRF4&STAT6)|(AhR&IRF4)|AhR",
"NFKB1_RelA",    "IKK",
"NFKB2",         "(NFKB1_RelA&STAT5)|NFKB1_RelA",
"NR4A1",         "(STAT6&ERK)",
"PI3K",          "(JAK2&RAS)|JAK2",
"PIP3",          "(PI3K&PTEN)",
"PRDM1",         "(AhR&IRF4&KLF4)",
"PTEN",          "(MEK1&MAGI1)",
"PTPN1",         "AhR",
"PU1_b1",        "(STAT6&ERK)|STAT6|(PU1_b2&STAT6&ERK)|(PU1_b2&STAT6)|PU1_b2",
"PU1_b2",        "(PU1_b1&STAT6&ERK)",
"RAF",           "RAS",
"RAS",           "SHC_GRB2_mSOS",
"SELL",          "(FOXO1&PRDM1&STAT6)",
"SHC_GRB2_mSOS", "CSF2R",
"SHP1",          "(USF1&LnC_DC)",
"SLAMF1",        "(ELK4&IRF4&STAT6)",
"SOCS",          "(STAT3_b1&STAT3_b2)",
"STAT3_b1",      "JAK1|(STAT3_b2&JAK1)|STAT3_b2",
"STAT3_b2",      "(STAT3_b1&JAK1&SHP1)",
"STAT5",         "(JAK2&Src)|JAK2",
"STAT6",         "JAK3",
"Src",           "(CSF2R&JAK2)|CSF2R",
"TAU",           "ERK",
"TIMP3",         "(AP1&IRF4&STAT6)",
"TLR3",          "(IRF4&PRDM1)|IRF4",
"TLR4",          "(AP1&IRF4&PRDM1&PU1_b1)|(AP1&IRF4&PRDM1)|(AP1&IRF4)|AP1",
"TLR6",          "(CEBPa&CEBPb&STAT6)|(CEBPa&CEBPb)|CEBPa",
"TLR7",          "(CEBPa&CEBPb&IRF4)|(CEBPa&CEBPb)|CEBPa",
"TLR8",          "(BATF3&CEBPa&KLF4&STAT6)|(BATF3&CEBPa&KLF4)|(BATF3&CEBPa)|BATF3",
"Tet2",          "PU1_b1",
"USF1",          "(KLF4&PU1_b1)|KLF4",
"cMYC",          "(ERK&GSK3B)",
"mTORC1",        "AKT"]

names = list[::2]
values = list[1::2]

# creating the graph with vertices = # of nodes in table and no edges
dend = Graph(directed = True)
dend.add_vertices(len(names))
dend.vs["name"] = names
# edges filled in by expanding via update table
table = [names,values]

exp_dend = update_expand.expand(dend, table)
# expansion is complete

# to obtain get back original graph, we remove composite nodes and replace
# with synergy
toadd = []
for edge in exp_dend.get_edgelist():
    if exp_dend.vs[edge[0]]["composite"]:

        toadd.append((exp_dend.predecessors(edge[0]), edge[1]))

# removes composite nodes
v = 0
toremove = []
while v < len(exp_dend.vs()):
    if exp_dend.vs[v]["composite"]:
        toremove.append(exp_dend.vs[v]["name"])
    v += 1
exp_dend.delete_vertices(toremove)

# adds synergy attribute to edges
tosynergize = []
for e in toadd:
    for comp in e[0]:
        tosynergize.append((comp,e[1]))
        exp_dend.add_edges([(comp,e[1])])
exp_dend.es["synergy"] = [0*len(exp_dend.es())]

i=0
ctr = 1
edgelist = exp_dend.get_edgelist()
while i<len(tosynergize):
    if (tosynergize[i][1] != tosynergize[i-1][1])&(i!=0):
        ctr +=1
    exp_dend.es[edgelist.index(tosynergize[i])]["synergy"] =ctr
    i+=1