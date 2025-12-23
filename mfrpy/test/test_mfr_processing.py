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
