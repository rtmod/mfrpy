import igraph as ig
from sympy.logic.boolalg import to_dnf
from mfrpy import sgmfr

dendrite = ig.Graph.Read_GraphML("sandbox/dendrite.gml")

# this results in an infinite loop
sgmfr.get_mfrs(dendrite, [32, 36], 29)
sgmfr.get_mfrs(dendrite, [32, 36], 29, verbose = 1)

dendrite = dendrite.simplify(multiple = False, loops = True)

# these don't
sgmfr.get_mfrs(dendrite, [32], 29)
sgmfr.get_mfrs(dendrite, [36], 29)
sgmfr.get_mfrs(dred, [dred.vs(name="CSF2")[0].index], dred.vs(name="NFKB2")[0].index)
sgmfr.get_mfrs(dred, [dred.vs(name="IL4")[0].index], dred.vs(name="NFKB2")[0].index)
# this one does
sgmfr.get_mfrs(dendrite, [32, 36], 29)
sgmfr.get_mfrs(dendrite, [32, 36], 29, mode = "el")

# reduce graph incrementally while preserving pathology
from copy import deepcopy
dred = deepcopy(dendrite)
name_rm = [
"CPLA2", "TAU", "CLIP1", "MAOA", "IL4_gene", "cMYC", "GSK3B", "FLT3", "Tet2",
"mTORC1", "SLAMF1", "ELK4", "DUOX1", "TIMP3", "ITGAX", "HLA_DR", "ALOX15",
"CIITA", "SOCS", "SHP1", "Lnc_DC", "MAFB", "FOS", "STAT3", "CEBPa", "FOXO1",
"NR4A1", "JAK1", "CREB", "TLR8", "TLR7", "TLR6", "TLR4", "TLR3", "SELL", "MERTK",
"DUSP6", "DEC205", "DCIR", "CD86", "CD83", "CD48", "CD40", "CD226", "CD209",
"CD206", "CD1C", "CD1B", "CD1A", "CD163", "CD141", "CD14", "CCL22", "CCL2",
"CCDC151", "BECN1", "JAK3", "Src", "LnC_DC", "SHC_GRB2_mSOS", "MAGI1", "PTEN",
"PI3K", "RAS", "JAK2", "PTPN1", "IL4R", "CSF2R", "MEK1", "BATF3", "PRDM1",
"ATF1", "STAT5", "CEBPb", "AP1", "BCL2", "JNK", "STAT3_b2", "JUN", "STAT3_b1",
"PIP3", "RAF"
]
for c in name_rm:
	dred.delete_vertices(dred.vs(name = c))

# manually iterate
for v in dred.vs:
	print(v)

#dred.delete_vertices(dred.vs(name = ""))
src = [dred.vs(name = "CSF2")[0].index, dred.vs(name = "IL4")[0].index]
tgt = dred.vs(name = "NFKB2")[0].index
sgmfr.get_mfrs(dred, src, tgt)

dred.write(f = "sandbox/dendrite.txt", format = "edgelist")
