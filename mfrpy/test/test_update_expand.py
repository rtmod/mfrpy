import unittest
from igraph import Graph
from sympy.logic.boolalg import Xnor
from mfrpy import update_expand, sgmfr
from mfrpy.examplegraphs import igraph_graph


class testing(unittest.TestCase):
    def test_acyclic_expansion(self):
        expanded_dag = update_expand.expand(
        igraph_graph.dag,
        update_expand.updates(igraph_graph.dag, igraph_graph.dag.es["synergy"], [])
        )
        assert expanded_dag.isomorphic(igraph_graph.exp_dag), "not isomorphic"

    def test_cyclic_expansion(self):
        expanded_dcg = update_expand.expand(
        igraph_graph.dcg,
        update_expand.updates(
        igraph_graph.dcg, igraph_graph.dcg.es["synergy"], []
        ))
        assert expanded_dcg.isomorphic(igraph_graph.exp_dcg), "not isomorphic"

    def test_update_table(self):
        correct = [
        ("i", ""), ("a", "i"), ("b", "(i&d)"), ("c", "i"),
        ("d", "c|e"), ("e", "(a&b)|f"), ("f", "d"), ("o", "e|f")
        ]
        actual = []
        i = 0
        obtained = update_expand.updates(
        igraph_graph.dcg, igraph_graph.dcg.es["synergy"], []
        )
        while i < len(obtained[0]):
            actual.append((obtained[0][i],
            obtained[1][i]))
            i+=1
        for pair in correct:
            for couple in actual:
                if (pair[0] == couple[0]) and (pair[1]):
                    assert Xnor(pair[1], couple[1]), "expressions not equivalent"

    def test_involution(self):
        synergies_and_edges = [[1, 2, 3, 4, 5], [
        [(2, 4), (1, 4)], [(2, 4), (3, 4)],
        [(0, 1)], [(0, 2)], [(0, 3)]
        ]]
        edges_and_synergies = [[
        (0, 1), (0, 2), (0, 3), (1, 4),
        (2, 4), (3, 4)],
        [[3], [4], [5], [1], [1, 2], [2]
        ]]
        #assert set(update_expand.involution(synergies_and_edges)[1]) == set(edges_and_synergies[1])
        #assert update_expand.involution(edges_and_synergies) == synergies_and_edges
        assert update_expand.involution(
        update_expand.involution(synergies_and_edges)) == synergies_and_edges

    def test_priming(self):
        syns = [3,4,5,1,1,2,2]
        edgelist = [
            (0,1), (0,2), (0,3), (1,4),
            (2,4), (2,4), (3,4)
            ]
        correct = []
        actual = []
        i = 0
        while i < len(edgelist):
            correct.append((edgelist[i], syns[i]))
            i += 1
        j = 0
        while j < len(update_expand.prime(igraph_graph.manysyns)[0][0]):
            actual.append((
            update_expand.prime(igraph_graph.manysyns)[0][0][j],
            update_expand.prime(igraph_graph.manysyns)[0][1][j]
            ))
            j += 1
        assert set(actual) == set(correct), "edge-synergy pairs do not match"

    def test_sgmfr(self):
        pass

if __name__ == '__main__':
    unittest.main()
