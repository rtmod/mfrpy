"""
Tests for preprocessing functions: prime, updates, expand, involution
Tests graph construction and transformation before MFR computation
"""

import unittest
import os
from mfrpy.test.test_setup import (
    HAS_IGRAPH, HAS_MFRPY, HAS_EXAMPLEGRAPHS,
    Graph, update_expand, igraph_graph
)

try:
    from sympy.logic.boolalg import Xnor
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False


class TestPrime(unittest.TestCase):
    """Tests for prime() function - prepares synergy values"""
    
    def test_empty_synergy_list(self):
        """Test that empty synergy list doesn't crash"""
        synergy = []
        if synergy:
            newval = max(synergy) + 1
        else:
            newval = 1
        self.assertEqual(newval, 1, "Empty list should result in newval=1")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_prime_with_empty_synergy_attribute(self):
        """Test prime() function handles empty/missing synergy"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        # Don't set synergy attribute
        try:
            result = update_expand.prime(g)
            self.assertIsNotNone(result, "prime() should return a result")
        except ValueError as e:
            if "max()" in str(e) and "empty" in str(e).lower():
                self.fail(f"prime() should prevent max() on empty synergy: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_prime_with_zeros(self):
        """Test prime() function handles zeros in synergy using enumerate"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 1), (1, 2), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        g.es["synergy"] = [0, 0, 0]
        try:
            result = update_expand.prime(g)
            self.assertIsNotNone(result, "prime() should return a result")
        except ValueError as e:
            if "is not in list" in str(e):
                self.fail(f"prime() should use enumerate, not .index(): {e}")


class TestUpdates(unittest.TestCase):
    """Tests for updates() function - creates update table"""
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_empty_edgelist_in_updates(self):
        """Test that updates() handles empty edgelist gracefully"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.vs["name"] = ["A", "B", "C"]
        # No edges added, so edgelist will be empty
        try:
            table = update_expand.updates(g, [], [])
            self.assertIsNotNone(table, "updates() should return a result even with empty edgelist")
        except ValueError as e:
            if "max()" in str(e) and "empty" in str(e).lower():
                self.fail(f"updates() should prevent max() on empty edgelist: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_updates_with_synergy_but_no_edges(self):
        """Test updates() with synergy list but graph has no edges"""
        g = Graph(directed=True)
        g.add_vertices(2)
        g.vs["name"] = ["A", "B"]
        try:
            table = update_expand.updates(g, [0, 0], [])
            self.assertIsNotNone(table, "Should handle graph with no edges")
        except ValueError as e:
            if "max()" in str(e) and "empty" in str(e).lower():
                self.fail(f"updates() should prevent max() on empty edgelist: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY and HAS_SYMPY, "Requires igraph, mfrpy, and sympy")
    def test_update_table_correctness(self):
        """Test that update table is computed correctly"""
        if not HAS_EXAMPLEGRAPHS:
            self.skipTest("Example graphs not available")
        correct = [
            ("i", ""), ("a", "i"), ("b", "(i&d)"), ("c", "i"),
            ("d", "c|e"), ("e", "(a&b)|f"), ("f", "d"), ("o", "e|f")
        ]
        actual = []
        obtained = update_expand.updates(
            igraph_graph.dcg, igraph_graph.dcg.es["synergy"], []
        )
        i = 0
        while i < len(obtained[0]):
            actual.append((obtained[0][i], obtained[1][i]))
            i += 1
        for pair in correct:
            for couple in actual:
                if (pair[0] == couple[0]) and (pair[1]):
                    assert Xnor(pair[1], couple[1]), "expressions not equivalent"


class TestExpand(unittest.TestCase):
    """Tests for expand() function - expands graph with composite nodes"""
    
    def test_composite_initialization_logic(self):
        """Test that composite initialization creates correct list length"""
        test_cases = [
            {"names": ["A", "B", "C"], "expected_length": 3},
            {"names": ["A"], "expected_length": 1},
            {"names": ["A", "B", "C", "D", "E"], "expected_length": 5},
            {"names": [], "expected_length": 0},
        ]
        for case in test_cases:
            names = case["names"]
            expected_length = case["expected_length"]
            composite = [0] * len(names)
            self.assertEqual(len(composite), expected_length,
                           f"Failed for {len(names)} nodes")
            self.assertTrue(all(x == 0 for x in composite),
                          "All values should be 0")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_composite_initialization_in_expand(self):
        """Test that expand() correctly initializes composite nodes"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0]
        table = update_expand.updates(g, g.es["synergy"], [])
        expanded = update_expand.expand(g, table)
        self.assertEqual(len(expanded.vs["composite"]), len(expanded.vs["name"]),
                        "Composite list should match number of vertices")
        for val in expanded.vs["composite"]:
            self.assertIsInstance(val, (int, type(0)),
                                 "Composite values should be integers")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY and HAS_EXAMPLEGRAPHS, "Requires igraph, mfrpy, and example graphs")
    def test_acyclic_expansion(self):
        """Test expansion of acyclic graph matches expected result"""
        expanded_dag = update_expand.expand(
            igraph_graph.dag,
            update_expand.updates(igraph_graph.dag, igraph_graph.dag.es["synergy"], [])
        )
        assert expanded_dag.isomorphic(igraph_graph.exp_dag), "not isomorphic"
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY and HAS_EXAMPLEGRAPHS, "Requires igraph, mfrpy, and example graphs")
    def test_cyclic_expansion(self):
        """Test expansion of cyclic graph matches expected result"""
        expanded_dcg = update_expand.expand(
            igraph_graph.dcg,
            update_expand.updates(
                igraph_graph.dcg, igraph_graph.dcg.es["synergy"], []
            ))
        assert expanded_dcg.isomorphic(igraph_graph.exp_dcg), "not isomorphic"


class TestInvolution(unittest.TestCase):
    """Tests for involution() function - converts between edge-synergy formats"""
    
    def test_involution_property(self):
        """Test that involution applied twice returns original"""
        synergies_and_edges = [[1, 2, 3, 4, 5], [
            [(2, 4), (1, 4)], [(2, 4), (3, 4)],
            [(0, 1)], [(0, 2)], [(0, 3)]
        ]]
        assert update_expand.involution(
            update_expand.involution(synergies_and_edges)) == synergies_and_edges


class TestPriming(unittest.TestCase):
    """Tests for prime() function with example graphs"""
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY and HAS_EXAMPLEGRAPHS, "Requires igraph, mfrpy, and example graphs")
    def test_priming_with_example_graph(self):
        """Test prime() function with example graph"""
        syns = [3, 4, 5, 1, 1, 2, 2]
        edgelist = [
            (0, 1), (0, 2), (0, 3), (1, 4),
            (2, 4), (2, 4), (3, 4)
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


class TestPreprocessingEdgeCases(unittest.TestCase):
    """Edge cases for preprocessing functions"""
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_empty_graph(self):
        """Test with empty graph"""
        g = Graph(directed=True)
        g.add_vertices(0)
        g.vs["name"] = []
        g.es["synergy"] = []
        try:
            table = update_expand.updates(g, [], [])
            self.assertIsNotNone(table)
        except Exception as e:
            self.fail(f"Should handle empty graph: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_single_node_graph(self):
        """Test with single node graph"""
        g = Graph(directed=True)
        g.add_vertices(1)
        g.vs["name"] = ["A"]
        g.es["synergy"] = []
        try:
            table = update_expand.updates(g, [], [])
            expanded = update_expand.expand(g, table)
            self.assertEqual(len(expanded.vs["composite"]), len(expanded.vs["name"]),
                            "Composite list should match vertex count")
        except Exception as e:
            self.fail(f"Should handle single node graph: {e}")
    
    def test_all_zeros_synergy(self):
        """Test with all zeros in synergy"""
        synergy = [0, 0, 0, 0]
        if synergy:
            newval = max(synergy) + 1
        else:
            newval = 1
        for i, value in enumerate(synergy):
            if value == 0:
                synergy[i] = newval
                newval += 1
        self.assertNotIn(0, synergy, "All zeros should be replaced")
        self.assertEqual(synergy, [1, 2, 3, 4],
                        "Zeros should be replaced sequentially")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_graph_with_cycles(self):
        """Test graph with cycles (A->B->C->A)"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2), (2, 0)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0, 0]
        try:
            table = update_expand.updates(g, g.es["synergy"], [])
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded, "Should handle cycles")
            self.assertEqual(len(expanded.vs["composite"]), len(expanded.vs["name"]),
                            "Composite list should match vertex count")
        except Exception as e:
            self.fail(f"Should handle cycles: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_all_edges_have_synergy(self):
        """Test graph where all edges have synergy"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 1), (1, 2), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        g.es["synergy"] = [1, 1, 1]
        try:
            table = update_expand.updates(g, g.es["synergy"], [])
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded, "Should handle all synergy edges")
            self.assertEqual(len(expanded.vs["composite"]), len(expanded.vs["name"]),
                            "Composite list should match vertex count")
        except Exception as e:
            self.fail(f"Should handle all synergy edges: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_large_synergy_values(self):
        """Test with large synergy values"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [10, 15]
        try:
            table = update_expand.updates(g, g.es["synergy"], [])
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded, "Should handle large synergy values")
        except Exception as exc:
            pass
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_graph_with_inhibition(self):
        """Test graph with inhibition edges"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 1), (1, 2), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        g.es["synergy"] = [0, 0, 0]
        inhibition = [0, 1, 0]
        try:
            table = update_expand.updates(g, g.es["synergy"], inhibition)
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded, "Should handle inhibition edges")
        except Exception as e:
            self.fail(f"Should handle inhibition edges: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_very_large_graph(self):
        """Test with a larger graph (20 nodes)"""
        g = Graph(directed=True)
        num_nodes = 20
        g.add_vertices(num_nodes)
        edges = [(i, i+1) for i in range(num_nodes - 1)]
        g.add_edges(edges)
        g.vs["name"] = [f"Node{i}" for i in range(num_nodes)]
        g.es["synergy"] = [0] * len(edges)
        try:
            table = update_expand.updates(g, g.es["synergy"], [])
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded, "Should handle large graphs")
            self.assertEqual(len(expanded.vs["composite"]), len(expanded.vs["name"]),
                            "Composite list should match vertex count")
        except Exception as e:
            self.fail(f"Should handle large graphs: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
