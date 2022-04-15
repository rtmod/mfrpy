"""
Module for expanding a graph with synergistic and inhibitory edges
"""

from igraph import *

def expand_graph(graph, synergy = []):
    """
    Given a graph and the synergy of its edges, return the expanded graph with
    composite nodes

    Uses *python-igraph*:
    http://igraph.org/python/

    Parameters:
    graph  -- *igraph* Graph object
    synergy -- list of synergy values of the edge sequence

    """
    # if no synergy is provided then graph is already expanded
    if not synergy:
        # graph.composite_nodes = []
        graph.vs["composite"] = [0] * graph.vcount()
        return graph
    # creates a new expanded graph
    else:
        # initialization
        exp_graph = Graph(directed = True)
        # exp_graph.composite_nodes = []
        startcount = graph.vcount()
        names = graph.vs["name"]
        edgelist = graph.get_edgelist()

        # expanded graph has composite node attribute
        indices = []
        i = 1
        # finds indices of edges with synergy
        while i <= max(graph.es["synergy"]):
            indices.append(
            [syn for syn,val in enumerate(graph.es["synergy"]) if val==i])
            i += 1
        all_indices = [item for index in indices for item in index]

        # creates list of edges with synergy
        synergies = []
        for ind in indices:
            syn = [list(edgelist[i]) for i in ind]
            synergies.append(syn)

        # adds new vertices
        for i in range(len(indices)):
            graph.add_vertices(1)
            i += 1
        endcount = graph.vcount()

        # deletes previous synergistic edges
        tochange = []
        for ind in all_indices:
            tochange.append(edgelist[ind])
        for item in tochange:
            edgelist.remove(item)

        # gives names to new composite nodes
        i = 1
        for v in range(startcount, endcount):
            name = "c{}".format(i)
            i += 1
            names.append(name)
            # exp_graph.composite_nodes.append(v)

        synstems = []
        stalks = []
        # appends new edges between composite nodes to replace synergy
        for syn in synergies:
            synstems.append([sub[0] for sub in syn])
            stalks.append(syn[0][1])
        i = 1
        for block in synstems:
            for node in block:
                edgelist.append((node, startcount -1 + i))
            i += 1
        i = 1
        for node in stalks:
            edgelist.append((startcount - 1 + i, node))
            i += 1

        # finalizes the graph
        exp_graph.add_vertices(graph.vcount())
        exp_graph.add_edges(edgelist)
        exp_graph.vs["name"] = names
        exp_graph.vs["composite"] = [0]
        for i in range(startcount, endcount):
            exp_graph.vs[i]["composite"] = 1

        return exp_graph

        # implement inhibitory edge expansion function
        # implement contraction function
