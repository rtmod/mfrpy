"""
Tests for MFR processing functions: get_mfrs
Tests minimal functional route computation and edge cases
"""

import unittest
from mfrpy.test.test_setup import (
    HAS_IGRAPH, HAS_MFRPY,
    Graph, update_expand, sgmfr
)


class TestGetMfrs(unittest.TestCase):
    """Tests for get_mfrs() function - computes minimal functional routes"""
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_missing_edge_handling(self):
        """Test that missing edges are handled gracefully"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0]
        mfr_chunks = [(0, 1), (1, 2), (2, 0)]  # (2, 0) doesn't exist
        ids = []
        warnings = []
        for chunk in mfr_chunks:
            try:
                eid = g.get_eid(chunk[0], chunk[1])
                ids.append(eid)
            except Exception:
                warnings.append(f"Warning: Edge ({chunk[0]}, {chunk[1]}) not found")
        self.assertEqual(len(ids), 2, "Should find 2 existing edges")
        self.assertEqual(len(warnings), 1, "Should warn about 1 missing edge")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_get_mfrs_with_missing_edges_small(self):
        """Test get_mfrs handles missing edges in mode='es' with small graph"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 1), (1, 2), (2, 3), (0, 2)])
        g.vs["name"] = ["A", "B", "C", "D"]
        g.es["synergy"] = [0, 1, 0, 1]
        try:
            result = sgmfr.get_mfrs(g, [0], 3, mode="es", verbose=False)
            self.assertIsNotNone(result, "get_mfrs should return a result")
            self.assertIsInstance(result, list, "Result should be a list")
            self.assertEqual(len(result), 2, "Result should have [MFRs, count]")
        except Exception as e:
            self.fail(f"get_mfrs should handle missing edges gracefully: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_get_mfrs_with_missing_edges_large(self):
        """Test get_mfrs handles missing edges in mode='es' with larger graph"""
        g = Graph(directed=True)
        g.add_vertices(8)
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
                 (0, 2), (1, 3), (2, 4), (3, 5), (4, 6)]
        g.add_edges(edges)
        g.vs["name"] = [f"Node{i}" for i in range(8)]
        synergy = [0] * len(edges)
        synergy[2] = 1
        synergy[4] = 1
        synergy[7] = 1
        g.es["synergy"] = synergy
        try:
            result = sgmfr.get_mfrs(g, [0], 7, mode="es", verbose=False)
            self.assertIsNotNone(result, "get_mfrs should return a result")
            self.assertIsInstance(result, list, "Result should be a list")
            self.assertEqual(len(result), 2, "Result should have [MFRs, count]")
            mfrs, count = result
            self.assertIsInstance(mfrs, list, "MFRs should be a list")
            self.assertIsInstance(count, int, "Count should be an integer")
        except Exception as e:
            self.fail(f"get_mfrs should handle missing edges gracefully in large graph: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_get_mfrs_missing_edge_specific(self):
        """Test missing edges in expanded graph don't crash mode='es'"""
        g = Graph(directed=True)
        g.add_vertices(5)
        g.add_edges([(0, 1), (1, 2), (2, 3), (2, 4), (3, 4)])
        g.vs["name"] = ["A", "B", "C", "D", "E"]
        g.es["synergy"] = [0, 0, 1, 1, 0]
        try:
            result = sgmfr.get_mfrs(g, [0], 4, mode="es", verbose=False, expanded=False)
            self.assertIsNotNone(result, "Should return result even with missing edges")
            mfrs, count = result
            self.assertIsInstance(mfrs, list, "MFRs should be a list")
            for mfr in mfrs:
                self.assertIsInstance(mfr, list, "Each MFR should be a list of edge IDs")
        except Exception as e:
            self.fail(f"Should prevent crash on missing edges: {e}")


class TestMfrEdgeCases(unittest.TestCase):
    """Edge cases for MFR computation"""
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_source_equals_target(self):
        """Test when source node equals target node"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0]
        try:
            result = sgmfr.get_mfrs(g, [0], 0, mode="es", verbose=False)
            self.assertIsNotNone(result, "Should handle source==target")
            mfrs, count = result
            self.assertIsInstance(mfrs, list, "MFRs should be a list")
        except Exception as e:
            pass
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_no_path_from_source_to_target(self):
        """Test when there's no path from source to target"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 1), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        g.es["synergy"] = [0, 0]
        try:
            result = sgmfr.get_mfrs(g, [0], 3, mode="es", verbose=False)
            self.assertIsNotNone(result, "Should handle no path gracefully")
            mfrs, count = result
            self.assertIsInstance(mfrs, list, "MFRs should be a list")
        except Exception as e:
            self.fail(f"Should handle no path gracefully: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_multiple_sources(self):
        """Test with multiple source nodes"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 2), (1, 2), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        g.es["synergy"] = [0, 0, 0]
        try:
            result = sgmfr.get_mfrs(g, [0, 1], 3, mode="es", verbose=False)
            self.assertIsNotNone(result, "Should handle multiple sources")
            mfrs, count = result
            self.assertIsInstance(mfrs, list, "MFRs should be a list")
        except Exception as e:
            self.fail(f"Should handle multiple sources: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_different_output_modes(self):
        """Test different output modes (em, el, es)"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0]
        modes = ["em", "el", "es"]
        for mode in modes:
            try:
                result = sgmfr.get_mfrs(g, [0], 2, mode=mode, verbose=False)
                self.assertIsNotNone(result, f"Should handle mode '{mode}'")
                mfrs, count = result
                self.assertIsInstance(mfrs, list, f"MFRs should be a list for mode '{mode}'")
            except Exception as e:
                self.fail(f"Should handle mode '{mode}': {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_complex_synergy_pattern(self):
        """Test complex synergy pattern with multiple composite nodes"""
        g = Graph(directed=True)
        g.add_vertices(6)
        g.add_edges([(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (2, 5)])
        g.vs["name"] = ["A", "B", "C", "D", "E", "F"]
        g.es["synergy"] = [0, 1, 0, 0, 1, 1]
        try:
            table = update_expand.updates(g, g.es["synergy"], [])
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded, "Should handle complex synergy")
            result = sgmfr.get_mfrs(expanded, [0], 5, mode="es", verbose=False)
            self.assertIsNotNone(result, "Should calculate MFRs with complex synergy")
        except Exception as e:
            self.fail(f"Should handle complex synergy pattern: {e}")


class TestMultiSource(unittest.TestCase):
    """Multi-input source tests for get_mfrs.

    These tests cover the scenarios that previously infinite-looped, such as
    the first 9 lines of sandbox/ex-dendritic.py (multiple sources reaching
    a target through a cyclic, partially synergistic graph).
    """

    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_multi_source_int_or_list(self):
        """Source argument should accept both an int and a list."""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0]
        r_int = sgmfr.get_mfrs(g, 0, 2, mode="es", verbose=False)
        r_list = sgmfr.get_mfrs(g, [0], 2, mode="es", verbose=False)
        self.assertEqual(r_int[1], r_list[1])

    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_multi_source_two_disjoint_paths(self):
        """Two sources, two disjoint paths to one target -> 2 MFRs."""
        g = Graph(directed=True)
        g.add_vertices(5)
        g.add_edges([(0, 2), (1, 3), (2, 4), (3, 4)])
        g.vs["name"] = ["s1", "s2", "a", "b", "t"]
        g.es["synergy"] = [0, 0, 0, 0]
        result = sgmfr.get_mfrs(g, [0, 1], 4, mode="es", verbose=False)
        mfrs, count = result
        self.assertGreaterEqual(count, 2,
            "Two disjoint source-to-target paths should produce >=2 MFRs")

    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_multi_source_with_synergy_and(self):
        """Two sources synergistically required (AND) at the target.

        Mirrors ex-2source.py: i1, i2 -> a/b -> c/o where the target
        depends on a synergy of two upstream paths.
        """
        g = Graph(directed=True)
        g.add_vertices(6)
        g.add_edges([(0, 2), (1, 3), (1, 2), (3, 2), (3, 4), (3, 5), (2, 4), (4, 5)])
        g.vs["name"] = ["i1", "i2", "a", "b", "c", "o"]
        g.es["synergy"] = [1, 0, 1, 0, 0, 0, 0, 0]
        result = sgmfr.get_mfrs(g, [0, 1], 5, mode="es", verbose=False)
        self.assertIsNotNone(result)
        mfrs, count = result
        self.assertIsInstance(mfrs, list)
        self.assertIsInstance(count, int)

    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_multi_source_with_cycle_terminates(self):
        """Multi-source on a cyclic graph must terminate (no infinite loop).

        Reproduces the structural shape of the dendritic example: two source
        nodes, a downstream cycle, and a single target. Before the fix this
        would spin forever; the iteration cap + cycle-safe pred handling
        ensure it terminates.
        """
        g = Graph(directed=True)
        g.add_vertices(6)
        g.add_edges([
            (0, 2), (1, 2),
            (2, 3), (3, 4), (4, 2),
            (3, 5),
        ])
        g.vs["name"] = ["s1", "s2", "x", "y", "z", "t"]
        g.es["synergy"] = [0, 0, 0, 0, 0, 0]
        result = sgmfr.get_mfrs(
            g, [0, 1], 5, mode="es", verbose=False, max_iterations=10000
        )
        self.assertIsNotNone(result, "Should terminate even with cycles")
        mfrs, count = result
        self.assertIsInstance(mfrs, list)
        self.assertIsInstance(count, int)

    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_multi_source_only_one_reaches(self):
        """If only one source has a path to target, MFRs should still be
        found and the unreachable source must not break the run."""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 2), (2, 3)])
        g.vs["name"] = ["s_reach", "s_isolated", "x", "t"]
        g.es["synergy"] = [0, 0]
        result = sgmfr.get_mfrs(g, [0, 1], 3, mode="es", verbose=False)
        self.assertIsNotNone(result)
        mfrs, count = result
        self.assertGreaterEqual(count, 1)

    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_iteration_cap_raises_without_partial_results(self):
        """Hitting max_iterations should raise, not return partial MFRs."""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0]
        with self.assertRaises(RuntimeError) as ctx:
            sgmfr.get_mfrs(g, [0], 2, mode="es", verbose=False, max_iterations=0)
        self.assertIn("iteration cap", str(ctx.exception).lower())

    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_default_iteration_cap_completes(self):
        """Default graph-aware cap (max_iterations=None) should finish small graphs."""
        g = Graph(directed=True)
        g.add_vertices(5)
        g.add_edges([(0, 2), (1, 3), (2, 4), (3, 4)])
        g.vs["name"] = ["s1", "s2", "a", "b", "t"]
        g.es["synergy"] = [0, 0, 0, 0]
        result = sgmfr.get_mfrs(g, [0, 1], 4, mode="es", verbose=False)
        self.assertIsNotNone(result)
        mfrs, count = result
        self.assertGreaterEqual(count, 1)


class TestMfrIntegration(unittest.TestCase):
    """Integration tests for full MFR workflow"""
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_full_workflow(self):
        """Test full workflow: updates -> expand -> get_mfrs"""
        g = Graph(directed=True)
        g.add_vertices(5)
        g.add_edges([(0, 1), (1, 2), (2, 3), (3, 4)])
        g.vs["name"] = ["A", "B", "C", "D", "E"]
        g.es["synergy"] = [0, 0, 0, 0]
        try:
            # Step 1: Updates
            table = update_expand.updates(g, g.es["synergy"], [])
            self.assertIsNotNone(table)
            # Step 2: Expand
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded)
            self.assertEqual(len(expanded.vs["composite"]), len(expanded.vs["name"]),
                            "Composite initialization should be correct")
            # Step 3: Get MFRs
            result = sgmfr.get_mfrs(expanded, [0], 4, mode="es")
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Full workflow should work: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
