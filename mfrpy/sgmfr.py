"""
Bottom-up algorithm for finding minimal functional routes (MFRs)
"""

from igraph import Graph
import update_expand
from sympy.logic.boolalg import to_dnf

def get_mfrs(graph, source, target, verbose = False, mode = "es"):
    """
    Given a graph, source node, and target node, returns the number of MFRs
    from source to target and all MFRs.

    Uses *python-igraph*:
    http://igraph.org/python/

    Parameters:
    graph  -- *igraph* Graph object
    source -- integer index of source node
    target -- integer index of target node
    verbose -- option to diplay MFRs, defaults to False
    mode -- output option, defaults to "es"

    Supported output options:
    "em" -- returns edge matrices
    "el" -- returns edge lists
    "es" -- returns edge sequence indices

    """

    # Extract attributes from graph if they exist
    oggraph = graph
    try:
        synergistic = graph.es["synergy"]
    except KeyError:
        synergistic = []

    try:
        negatory = graph.es["inhibition"]
    except KeyError:
        negatory = []

    # Expansion of graph to include composite and inhibitory nodes
    graph = update_expand.expand(
        graph,
        update_expand.updates(graph, synergistic, negatory)
        )
    # Initialization of variables for main loop
    pointer = 0
    num = 1
    # tags is an array that keeps track of node indices in current MFR
    tags = [0]
    flag = False
    discard = []
    net = graph.get_adjlist(mode='in')
    all_MFRs = [[[target, net[target]]]]
    # redundant tracks nodes with no predecessors that are not the source
    redundant = []
    v = 0
    while v < len(graph.vs()):
        if not graph.predecessors(v):
            if not v == source:
                redundant.append(v)
        v += 1

    if verbose:
        print("nodes with no predecessors (other than source):", redundant)

    # Main loop, while some partial MFRs remain unfinished
    while pointer < num:
        flag = False
        c_MFR = all_MFRs[pointer]
        c_tag = tags[pointer]

        if verbose:
            print("current MFR:", all_MFRs[pointer])

        # While the current MFR is unfinished
        while not flag:
            c_node = c_MFR[c_tag][0]
            c_preds = c_MFR[c_tag][1]

            if verbose:
                print("node and predecessors:", c_node, c_preds)

            # If no predecessors remain
            # Note: python uses implicit booleans for lists
            if not c_preds:

                if verbose:
                    print("node", c_node, "has no predecessors")

                if c_tag == len(c_MFR) - 1:
                    flag = True

                    if verbose:
                        print("MFR finished")

                else:
                    c_tag = c_tag + 1

            else:
                # If current node is not composite
                if not graph.vs[c_node]["composite"]:
                    m = len(c_preds)
                    c_MFR[c_tag][1] = c_preds[0]
                    # Allots memory to new partial MFRs
                    i = 0
                    while i < m - 1:
                        # Creates a copy of the current MFR for each predecessor
                        temp1 = [li[:] for li in c_MFR]
                        temp1[c_tag][1] = [c_preds[i + 1]]
                        # Current MFR is replaced by first copy
                        all_MFRs.append(temp1)
                        tags.append(c_tag)
                        i = i + 1
                    num = num + m - 1
                    c_preds = [c_MFR[c_tag][1]]

                # List of entries in MFR's first "column" (from nodes)
                stems = [row[0] for row in c_MFR]
                # Checks that all c_preds are in c_MFR
                if not set(c_preds).difference(set(stems)):

                    if verbose:
                        print("all predecessors are in current MFR")

                    if c_tag == len(c_MFR) - 1:
                        flag = True

                        if verbose:
                            print("MFR finished")

                    else:
                        c_tag = c_tag + 1

                # Appends new rows to current partial MFR
                else:
                    for v in c_preds:
                        temp2 = net[v]

                        if verbose:
                            print("preds of preds:", temp2)

                        # If the node cannot be activated we ignore this MFR
                        if set(temp2).intersection(set(redundant)):
                            if graph.vs[v]["composite"]:
                                flag = True

                                if verbose:
                                    print("node can't be activated")

                                discard.append(c_MFR)
                        else:
                            c_MFR.append([v, temp2])
                    c_tag = c_tag + 1

                    if verbose:
                        print("new partial MFR:", c_MFR)

        pointer = pointer + 1

        # list of entries in MFRs second "column" (to nodes)
        stalks = [row[1] for row in c_MFR]
        # checks for impossible edges and adds extraneous MFRs to discard
        if not [] in stalks:
            discard.append(c_MFR)

        if verbose:
            print("discard:", discard)

    # Removes extra MFRs from cycles in graph or in discard list
    final_MFRs = []
    for mfr in all_MFRs:
        if not mfr in discard:
            final_MFRs.append(mfr)

    for mfr in final_MFRs:
        # Removes unecessary last row of MFR
        for item in mfr:
            if item == [0,[]]:
                mfr.remove(item)
        # Reverses order of lists (since algorithm is bottom-up)
        mfr.reverse()
        for item in mfr:
            item.reverse()
        # Flattens list
        for item in mfr:
            if type(item[0]) is list:
                for i in item[0]:
                    mfr.insert(mfr.index(item) + 1, [i, item[1]])
                mfr.remove(item)

    # Translates expanded vertices to original
    contracted_MFRs = []
    for mfr in final_MFRs:
        new_mfr = []

        if verbose:
            print("old mfr:", mfr)

        for edge in mfr:
            # Contracts composite edges by deleting composite nodes
            if graph.vs[edge[0]]["composite"]:
                for e in mfr:
                    if e[1] == edge[0]:
                        new_mfr.append([e[0], edge[1]])
            elif graph.vs[edge[1]]["composite"]:
                pass
            else:
                new_mfr.append(edge)

        # Changes inhibitory nodes back to originals
        for edge in new_mfr:
            if '~' in graph.vs[edge[0]]["name"]:
                dict = {edge[0]:graph.vs["name"].index(
                "{}".format(to_dnf("~{}".format(
                graph.vs[edge[0]]["name"]
                ))))}
                edge[0]=dict[edge[0]]
            elif '~' in graph.vs[edge[1]]["name"]:
                dict = {edge[1]:graph.vs["name"].index(
                "{}".format(to_dnf("~{}".format(
                graph.vs[edge[1]]["name"]
                ))))}
                edge[1]=dict[edge[1]]
        contracted_MFRs.append(new_mfr)

        if verbose:
            print("new mfr:", new_mfr)

    final_MFRs = contracted_MFRs

    if verbose:
        print("Number of MFRs:", len(final_MFRs))

    # Output options
    if mode == "em": # "em" = edge matrix
        ind = 1
        for mfr in final_MFRs:

            if verbose:
                print("\n", ind, ":")
                for chunk in mfr:
                    print(chunk)

            ind += 1
        return [final_MFRs, len(final_MFRs)]

    elif mode == "el": # "el" = edge list
        ind = 1
        for mfr in final_MFRs:

            if verbose:
                print("\n", ind, ":", mfr)

            ind += 1
        return [final_MFRs, len(final_MFRs)]

    elif mode == "es": # "es" = edge sequence ids
        ids = []
        ind = 1
        for mfr in final_MFRs:
            id = []
            for chunk in mfr:
                id.append(oggraph.get_eid(chunk[0], chunk[1]))
                id.sort()
            ids.append(id)

        if verbose:
            for id in ids:
                print(ind, ":", id, "\n")
                ind += 1

        return [ids, len(ids)]
