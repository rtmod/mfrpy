
from mfrpy import alg3, expand_contract
from mfrpy.examplegraphs import igraph_graph

def test_get_mfrs():
    dag = igraph_graph.dag()
    dag_mfrs = alg3.get_mfrs(dag, 0, 7)


def test_expand_graph():
    dcg = igraph_graph.dcg()
    expaned_dcg = expand_contract.expand_graph(dcg)
    assert expanded_dcg.isomorphic(igraph_graph.exp_dcg())
