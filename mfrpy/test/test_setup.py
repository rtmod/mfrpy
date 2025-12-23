"""
Common setup code for all test files
Handles imports and path setup
"""

import unittest
import sys
import os

# Add parent directory to path for development mode (when package isn't installed)
# This allows tests to run both when mfrpy is installed and when running from source
# Handle both script execution (has __file__) and interactive shell (no __file__)
try:
    # __file__ only exists when running as a script, not in interactive shells
    test_file = __file__
    parent_dir = os.path.join(os.path.dirname(test_file), '../..')
    parent_dir = os.path.abspath(parent_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
except NameError:
    # __file__ doesn't exist in interactive shells (like Sublime's Python console)
    # In this case, we rely on mfrpy being installed or the user setting up the path manually
    # Try to add current directory and parent directories as fallback
    current_dir = os.getcwd()
    possible_paths = [
        current_dir,
        os.path.join(current_dir, '..'),
        os.path.join(current_dir, '../..'),
    ]
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if abs_path not in sys.path:
            sys.path.insert(0, abs_path)

try:
    from igraph import Graph
    HAS_IGRAPH = True
except ImportError:
    HAS_IGRAPH = False
    Graph = None
    print("Warning: igraph not available. Some tests will be skipped.")

try:
    from mfrpy import update_expand, sgmfr
    HAS_MFRPY = True
except ImportError:
    HAS_MFRPY = False
    update_expand = None
    sgmfr = None
    print("Warning: mfrpy modules not available. Some tests will be skipped.")
    print("  Try: pip install -e .  (to install in development mode)")
    print("  Or ensure mfrpy is installed: pip install .")

try:
    from mfrpy.examplegraphs import igraph_graph
    HAS_EXAMPLEGRAPHS = True
except (ImportError, FileNotFoundError):
    HAS_EXAMPLEGRAPHS = False
    igraph_graph = None
    print("Warning: mfrpy.examplegraphs not available. Some tests will be skipped.")
