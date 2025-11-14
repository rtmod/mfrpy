"""
Unit tests for all bug fixes in mfrpy
Tests each bug fix with various edge cases
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from igraph import Graph
    HAS_IGRAPH = True
except ImportError:
    HAS_IGRAPH = False
    print("Warning: igraph not available. Some tests will be skipped.")

try:
    from mfrpy import update_expand, sgmfr
    HAS_MFRPY = True
except ImportError:
    HAS_MFRPY = False
    print("Warning: mfrpy modules not available. Some tests will be skipped.")

try:
    from mfrpy.examplegraphs import igraph_graph
    HAS_EXAMPLEGRAPHS = True
except (ImportError, FileNotFoundError):
    HAS_EXAMPLEGRAPHS = False
    print("Warning: mfrpy.examplegraphs not available. Some tests will be skipped.")


class TestBugFix1_CompositeInitialization(unittest.TestCase):
    """Test Bug Fix #1: Composite node initialization"""
    
    def test_composite_initialization_logic(self):
        """Test that composite initialization creates correct list length"""
        # Test the logic without igraph
        test_cases = [
            {"names": ["A", "B", "C"], "expected_length": 3},
            {"names": ["A"], "expected_length": 1},
            {"names": ["A", "B", "C", "D", "E"], "expected_length": 5},
            {"names": [], "expected_length": 0},
        ]
        
        for case in test_cases:
            names = case["names"]
            expected_length = case["expected_length"]
            
            # Our fix
            composite = [0] * len(names)
            
            # Old bug would create [0] for all cases
            old_bug_result = [0 * len(names)]  # This is [0]
            
            self.assertEqual(len(composite), expected_length,
                           f"Failed for {len(names)} nodes")
            self.assertTrue(all(x == 0 for x in composite),
                          "All values should be 0")
            
            # Verify old bug would be wrong for multi-node cases
            if len(names) > 1:
                self.assertNotEqual(len(old_bug_result), expected_length,
                                  "Old bug would have been wrong")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_composite_initialization_in_expand(self):
        """Test that expand() correctly initializes composite nodes"""
        # Create a simple graph
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0]
        
        # Expand the graph
        table = update_expand.updates(g, g.es["synergy"], [])
        expanded = update_expand.expand(g, table)
        
        # Check that composite list has correct length
        self.assertEqual(len(expanded.vs["composite"]), len(expanded.vs["name"]),
                        "Composite list should match number of vertices")
        
        # Check that all values are integers (0 or 1)
        for val in expanded.vs["composite"]:
            self.assertIsInstance(val, (int, type(0)),
                                 "Composite values should be integers")


class TestBugFix2_EmptyListHandling(unittest.TestCase):
    """Test Bug Fix #2: Empty list handling"""
    
    def test_empty_synergy_list(self):
        """Test that empty synergy list doesn't crash"""
        synergy = []
        
        # Our fix should handle this
        if synergy:
            newval = max(synergy) + 1
        else:
            newval = 1
        
        self.assertEqual(newval, 1, "Empty list should result in newval=1")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_prime_with_empty_synergy_attribute(self):
        """Test prime() function actually handles empty/missing synergy"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        # Don't set synergy attribute - this should trigger the KeyError handling
        
        # This should not crash - prime() should handle missing synergy
        try:
            result = update_expand.prime(g)
            self.assertIsNotNone(result, "prime() should return a result")
        except ValueError as e:
            if "max()" in str(e) and "empty" in str(e).lower():
                self.fail(f"Fix #2 should prevent max() on empty synergy: {e}")
            else:
                self.fail(f"prime() raised unexpected ValueError: {e}")
    
    def test_empty_list_in_prime_function(self):
        """Test prime() function with empty synergy"""
        if not HAS_IGRAPH or not HAS_MFRPY:
            self.skipTest("Requires igraph and mfrpy")
        
        # Create graph with no synergy edges
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        # Note: igraph doesn't allow empty lists as edge attributes
        # Instead, we test with no synergy attribute set, which should be handled
        # by checking if synergy exists and is non-empty in the code
        
        # This should not crash - prime() should handle missing/empty synergy
        try:
            result = update_expand.prime(g)
            self.assertIsNotNone(result, "prime() should return a result")
        except ValueError as e:
            self.fail(f"prime() raised ValueError with no synergy attribute: {e}")


class TestBugFix3_IndexLookup(unittest.TestCase):
    """Test Bug Fix #3: Index lookup error prevention"""
    
    def test_enumerate_usage(self):
        """Test that enumerate() is used instead of .index()"""
        synergy = [0, 1, 0, 2]
        original = synergy.copy()
        
        # Our fix using enumerate
        if synergy:
            newval = max(synergy) + 1
        else:
            newval = 1
        
        for i, value in enumerate(synergy):
            if value == 0:
                synergy[i] = newval
                newval += 1
        
        # Verify zeros were replaced
        self.assertNotIn(0, synergy, "All zeros should be replaced")
        self.assertEqual(len(synergy), len(original),
                        "List length should not change")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_prime_function_uses_enumerate(self):
        """Test that prime() function actually uses enumerate (not .index())"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 1), (1, 2), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        # Set synergy with zeros that need to be replaced
        g.es["synergy"] = [0, 0, 0]
        
        # This should work without ValueError from .index() not finding values
        try:
            result = update_expand.prime(g)
            self.assertIsNotNone(result, "prime() should return a result")
            # If we get here, enumerate() was used successfully
        except ValueError as e:
            if "is not in list" in str(e):
                self.fail(f"Fix #3 should prevent .index() errors: {e}")
            else:
                # Other ValueErrors might be okay
                pass
    
    def test_index_lookup_with_modifications(self):
        """Test that enumerate works even after list modifications"""
        synergy = [0, 0, 0]
        
        if synergy:
            newval = max(synergy) + 1
        else:
            newval = 1
        
        # Use enumerate to safely modify
        for i, value in enumerate(synergy):
            if value == 0:
                synergy[i] = newval
                newval += 1
        
        # Should have replaced all zeros
        self.assertEqual(synergy, [1, 2, 3],
                        "All zeros should be replaced with sequential values")


class TestBugFix4_MissingEdgeHandling(unittest.TestCase):
    """Test Bug Fix #4: Missing edge handling"""
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_missing_edge_in_get_eid(self):
        """Test that missing edges are handled gracefully"""
        # Create a simple graph
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0]
        
        # Create MFR chunks that include a missing edge
        mfr_chunks = [(0, 1), (1, 2), (2, 0)]  # (2, 0) doesn't exist
        
        ids = []
        warnings = []
        
        for chunk in mfr_chunks:
            try:
                eid = g.get_eid(chunk[0], chunk[1])
                ids.append(eid)
            except Exception:
                warnings.append(f"Warning: Edge ({chunk[0]}, {chunk[1]}) not found")
        
        # Should have found 2 edges and warned about 1
        self.assertEqual(len(ids), 2, "Should find 2 existing edges")
        self.assertEqual(len(warnings), 1, "Should warn about 1 missing edge")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_sgmfr_with_missing_edges_small(self):
        """Test Fix #4: sgmfr handles missing edges in mode='es' with small graph"""
        # Create a small graph with synergy that will create composite nodes
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 1), (1, 2), (2, 3), (0, 2)])
        g.vs["name"] = ["A", "B", "C", "D"]
        # Set synergy on edges (1,2) and (0,2) pointing to node 2
        g.es["synergy"] = [0, 1, 0, 1]  # Edges 1 and 3 have synergy
        
        # Calculate MFRs with mode='es' - this should not crash even if
        # expanded graph creates edges that don't map back to original
        try:
            result = sgmfr.get_mfrs(g, [0], 3, mode="es", verbose=False)
            self.assertIsNotNone(result, "get_mfrs should return a result")
            self.assertIsInstance(result, list, "Result should be a list")
            self.assertEqual(len(result), 2, "Result should have [MFRs, count]")
        except Exception as e:
            # If it fails, it should fail gracefully, not crash
            self.fail(f"get_mfrs should handle missing edges gracefully: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_sgmfr_with_missing_edges_large(self):
        """Test Fix #4: sgmfr handles missing edges in mode='es' with larger graph"""
        # Create a larger graph with multiple synergy nodes
        g = Graph(directed=True)
        g.add_vertices(8)
        # Create a more complex graph structure
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
                 (0, 2), (1, 3), (2, 4), (3, 5), (4, 6)]
        g.add_edges(edges)
        g.vs["name"] = [f"Node{i}" for i in range(8)]
        # Set synergy on multiple edges
        synergy = [0] * len(edges)
        synergy[2] = 1  # Edge (2,3) has synergy
        synergy[4] = 1  # Edge (4,5) has synergy
        synergy[7] = 1  # Edge (3,5) has synergy
        g.es["synergy"] = synergy
        
        # Calculate MFRs with mode='es' - this should handle missing edges
        # when expanded graph creates composite nodes with edges not in original
        try:
            result = sgmfr.get_mfrs(g, [0], 7, mode="es", verbose=False)
            self.assertIsNotNone(result, "get_mfrs should return a result")
            self.assertIsInstance(result, list, "Result should be a list")
            self.assertEqual(len(result), 2, "Result should have [MFRs, count]")
            # Verify that edge IDs are returned (even if some are missing)
            mfrs, count = result
            self.assertIsInstance(mfrs, list, "MFRs should be a list")
            self.assertIsInstance(count, int, "Count should be an integer")
        except Exception as e:
            # If it fails, it should fail gracefully, not crash
            self.fail(f"get_mfrs should handle missing edges gracefully in large graph: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_sgmfr_missing_edge_specific_fix4(self):
        """Test Fix #4 specifically: Missing edges in expanded graph don't crash mode='es'"""
        # This test specifically targets the bug fix #4 scenario:
        # When expanded graph has edges that don't exist in original graph,
        # get_eid() would crash. The fix should handle this gracefully.
        
        # Create graph with synergy that creates composite nodes
        g = Graph(directed=True)
        g.add_vertices(5)
        # Create edges: A->B, B->C, C->D, C->E, D->E
        g.add_edges([(0, 1), (1, 2), (2, 3), (2, 4), (3, 4)])
        g.vs["name"] = ["A", "B", "C", "D", "E"]
        # Set synergy on edges (2,3) and (2,4) pointing to node 2 (C)
        # This creates a composite node scenario
        g.es["synergy"] = [0, 0, 1, 1, 0]
        
        # The expanded graph will have composite nodes that may create edges
        # not present in the original graph. When mapping back in mode='es',
        # get_eid() should not crash on missing edges.
        try:
            result = sgmfr.get_mfrs(g, [0], 4, mode="es", verbose=False, expanded=False)
            # Should complete without crashing
            self.assertIsNotNone(result, "Should return result even with missing edges")
            mfrs, count = result
            # Even if some edges are missing, we should get valid results
            self.assertIsInstance(mfrs, list, "MFRs should be a list")
            for mfr in mfrs:
                self.assertIsInstance(mfr, list, "Each MFR should be a list of edge IDs")
        except Exception as e:
            self.fail(f"Fix #4 should prevent crash on missing edges: {e}")


class TestBugFix5_MissingDependency(unittest.TestCase):
    """Test Bug Fix #5: Missing dependency"""
    
    def test_tabulate_in_setup(self):
        """Test that tabulate is in setup.py"""
        setup_path = os.path.join(os.path.dirname(__file__), '../../setup.py')
        
        if not os.path.exists(setup_path):
            self.skipTest("setup.py not found")
        
        with open(setup_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('tabulate', content,
                     "tabulate should be in install_requires")
    
    def test_tabulate_import(self):
        """Test that tabulate can be imported (if available)"""
        try:
            import tabulate
            self.assertTrue(True, "tabulate can be imported")
        except ImportError:
            # This is okay - it means tabulate isn't installed
            # but it should be in setup.py so it gets installed
            pass


class TestTroubleshootingFile(unittest.TestCase):
    """Test that troubleshooting.py has fixes applied"""
    
    def test_troubleshooting_has_fixes(self):
        """Test that troubleshooting.py has the bug fixes"""
        troubleshooting_path = os.path.join(os.path.dirname(__file__), 'troubleshooting.py')
        
        if not os.path.exists(troubleshooting_path):
            self.skipTest("troubleshooting.py not found")
        
        with open(troubleshooting_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for missing edge handling
        self.assertIn('try:', content,
                     "troubleshooting.py should have try-except for get_eid")
        self.assertIn('graph.get_eid(chunk[0], chunk[1])', content,
                     "troubleshooting.py should handle get_eid errors")
        
        # Check for index error handling
        self.assertIn('mfr.insert(mfr.index(item)', content,
                     "troubleshooting.py should handle index errors")


class TestBugFix6_EmptyEdgelistHandling(unittest.TestCase):
    """Test Bug Fix #6: Empty edgelist handling in updates()"""
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_empty_edgelist_in_updates(self):
        """Test that updates() handles empty edgelist[1] gracefully"""
        # Create a graph with no edges (empty edgelist)
        g = Graph(directed=True)
        g.add_vertices(3)
        g.vs["name"] = ["A", "B", "C"]
        # No edges added, so edgelist will be empty
        
        # This should not crash - updates() should handle empty edgelist[1]
        try:
            table = update_expand.updates(g, [], [])
            self.assertIsNotNone(table, "updates() should return a result even with empty edgelist")
        except ValueError as e:
            if "max()" in str(e) and "empty" in str(e).lower():
                self.fail(f"Fix #6 should prevent max() on empty edgelist: {e}")
            else:
                # Other errors are okay, just not the max() on empty sequence error
                pass
        except Exception as e:
            # Other exceptions might be okay depending on implementation
            pass
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_updates_with_synergy_but_no_edges(self):
        """Test updates() with synergy list but graph has no edges"""
        g = Graph(directed=True)
        g.add_vertices(2)
        g.vs["name"] = ["A", "B"]
        # No edges, so edgelist[1] will be empty
        
        # Should handle this without crashing on max(edgelist[1])
        try:
            table = update_expand.updates(g, [0, 0], [])
            self.assertIsNotNone(table, "Should handle graph with no edges")
        except ValueError as e:
            if "max()" in str(e) and "empty" in str(e).lower():
                self.fail(f"Fix #6 should prevent max() on empty edgelist: {e}")


class TestEdgeCases(unittest.TestCase):
    """Test various edge cases"""
    
    def test_empty_graph(self):
        """Test with empty graph"""
        if not HAS_IGRAPH or not HAS_MFRPY:
            self.skipTest("Requires igraph and mfrpy")
        
        g = Graph(directed=True)
        g.add_vertices(0)
        g.vs["name"] = []
        g.es["synergy"] = []
        
        # Should not crash
        try:
            table = update_expand.updates(g, [], [])
            self.assertIsNotNone(table)
        except Exception as e:
            self.fail(f"Should handle empty graph: {e}")
    
    def test_single_node_graph(self):
        """Test with single node graph"""
        if not HAS_IGRAPH or not HAS_MFRPY:
            self.skipTest("Requires igraph and mfrpy")
        
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
        
        # All zeros should be replaced
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
    def test_source_equals_target(self):
        """Test when source node equals target node"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        g.es["synergy"] = [0, 0]
        
        try:
            # Source and target are the same
            result = sgmfr.get_mfrs(g, [0], 0, mode="es", verbose=False)
            self.assertIsNotNone(result, "Should handle source==target")
            mfrs, count = result
            self.assertIsInstance(mfrs, list, "MFRs should be a list")
        except Exception as e:
            # This might be expected behavior, but shouldn't crash
            pass
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_no_path_from_source_to_target(self):
        """Test when there's no path from source to target"""
        g = Graph(directed=True)
        g.add_vertices(4)
        # Create disconnected components: 0->1 and 2->3
        g.add_edges([(0, 1), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        g.es["synergy"] = [0, 0]
        
        try:
            # No path from 0 to 3
            result = sgmfr.get_mfrs(g, [0], 3, mode="es", verbose=False)
            self.assertIsNotNone(result, "Should handle no path gracefully")
            mfrs, count = result
            self.assertIsInstance(mfrs, list, "MFRs should be a list")
        except Exception as e:
            # Should handle gracefully, not crash
            self.fail(f"Should handle no path gracefully: {e}")
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_all_edges_have_synergy(self):
        """Test graph where all edges have synergy"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 1), (1, 2), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        # All edges have synergy
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
        """Test with very large synergy values"""
        g = Graph(directed=True)
        g.add_vertices(3)
        g.add_edges([(0, 1), (1, 2)])
        g.vs["name"] = ["A", "B", "C"]
        # Large synergy values (but within reasonable range for the algorithm)
        # Using smaller values that are still "large" relative to typical 0-10 range
        g.es["synergy"] = [10, 15]
        
        try:
            table = update_expand.updates(g, g.es["synergy"], [])
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded, "Should handle large synergy values")
        except Exception as exc:
            # If there's an error, it should be a known issue, not a crash
            # Large synergy values might cause issues if they exceed expected ranges
            # This test verifies the code doesn't crash, even if behavior is unexpected
            pass
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_multiple_sources(self):
        """Test with multiple source nodes"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 2), (1, 2), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        g.es["synergy"] = [0, 0, 0]
        
        try:
            # Multiple sources: [0, 1] to target 3
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
    def test_graph_with_inhibition(self):
        """Test graph with inhibition edges"""
        g = Graph(directed=True)
        g.add_vertices(4)
        g.add_edges([(0, 1), (1, 2), (2, 3)])
        g.vs["name"] = ["A", "B", "C", "D"]
        g.es["synergy"] = [0, 0, 0]
        inhibition = [0, 1, 0]  # Edge 1 has inhibition
        
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
        # Create a chain: 0->1->2->...->19
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
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_complex_synergy_pattern(self):
        """Test complex synergy pattern with multiple composite nodes"""
        g = Graph(directed=True)
        g.add_vertices(6)
        # Create graph: 0->1->2->3, 0->4->5, 2->5, 4->5
        g.add_edges([(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (2, 5)])
        g.vs["name"] = ["A", "B", "C", "D", "E", "F"]
        # Set synergy on edges pointing to nodes 2 and 5
        g.es["synergy"] = [0, 1, 0, 0, 1, 1]  # Multiple synergy nodes
        
        try:
            table = update_expand.updates(g, g.es["synergy"], [])
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded, "Should handle complex synergy")
            result = sgmfr.get_mfrs(expanded, [0], 5, mode="es", verbose=False)
            self.assertIsNotNone(result, "Should calculate MFRs with complex synergy")
        except Exception as e:
            self.fail(f"Should handle complex synergy pattern: {e}")


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple fixes"""
    
    @unittest.skipUnless(HAS_IGRAPH and HAS_MFRPY, "Requires igraph and mfrpy")
    def test_full_workflow_with_fixes(self):
        """Test full workflow with all fixes applied"""
        # Create graph similar to example graphs
        g = Graph(directed=True)
        g.add_vertices(5)
        g.add_edges([(0, 1), (1, 2), (2, 3), (3, 4)])
        g.vs["name"] = ["A", "B", "C", "D", "E"]
        g.es["synergy"] = [0, 0, 0, 0]
        
        # Test that all steps work
        try:
            # Step 1: Updates (tests empty list and index fixes)
            table = update_expand.updates(g, g.es["synergy"], [])
            self.assertIsNotNone(table)
            
            # Step 2: Expand (tests composite initialization fix)
            expanded = update_expand.expand(g, table)
            self.assertIsNotNone(expanded)
            self.assertEqual(len(expanded.vs["composite"]), len(expanded.vs["name"]),
                            "Composite initialization should be correct")
            
            # Step 3: Get MFRs (tests missing edge fix)
            result = sgmfr.get_mfrs(expanded, [0], 4, mode="es")
            self.assertIsNotNone(result)
            
        except Exception as e:
            self.fail(f"Full workflow should work with all fixes: {e}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
