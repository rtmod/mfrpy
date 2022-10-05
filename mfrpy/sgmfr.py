"""
Bottom-up algorithm for finding minimal functional routes (MFRs)
"""

from igraph import Graph
from mfrpy import update_expand

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

    synergistic = []
    if 'synergy' in graph.es.attributes():
        synergistic = graph.es["synergy"]
    negatory = []
    if 'inhibition' in graph.es.attributes():
        negatory = graph.es["inhibition"]
    # expansion of graph to include composite and inhibitory nodes
    graph = update_expand.expand(graph, update_expand.updates(graph,
    synergistic, negatory))

    # initialization
    pointer = 0
    num = 1
    # tags is an array of integers that keeps track of the index of a node in
    # the current MFR
    tags = [0]
    flag = False
    discard = []
    net = graph.get_adjlist(mode='in')
    all_MFRs = [[[target, net[target]]]]

    #keeps track of nodes with no predecessors that are not the source
    redundant = []
    v = 0
    while v < len(graph.vs()):
        if not graph.predecessors(v):
            if not v == source:
                redundant.append(v)
        v += 1

    if verbose:
        print("nodes with no predecessors (other than source):", redundant)
        print("composite list:", graph.vs["composite"])
    # while some partial MFRs remain
    while pointer < num:

        flag = False
        c_MFR = all_MFRs[pointer]
        c_tag = tags[pointer]
        # while the current MFR is incomplete
        if verbose:
            print("current MFR:", all_MFRs[pointer])
        while not flag:
            c_node = c_MFR[c_tag][0]
            # c_preds is a list of integers
            c_preds = c_MFR[c_tag][1]
            for ele in redundant:
                if ele in c_preds:
                    c_preds.remove(ele)
            if verbose:
                print("node and predecessors:", c_node, c_preds)
            # if no predecessors remain
            # python uses implicit booleans for lists
            if not c_preds:
                if verbose:
                    print("node", c_node, "has no predecessors")
                if c_tag == len(c_MFR) - 1:
                    flag = True
                    #if not source in [row[0] for row in c_MFR]:
                        #discard.append(c_MFR)
                    if verbose:
                        print("MFR finished")
                else:
                    c_tag = c_tag + 1

            else:
                # if not c_node in graph.composite_nodes:
                if not graph.vs[c_node]["composite"]:
                    m = len(c_preds)
                    c_MFR[c_tag][1] = c_preds[0]

                    # allots memory to new partial MFRs
                    i = 0
                    while i < m - 1:
                        # creates a copy of the current MFR for each predecessor
                        temp1 = [li[:] for li in c_MFR]
                        temp1[c_tag][1] = [c_preds[i + 1]]
                        # current MFR is replaced by first copy
                        all_MFRs.append(temp1)
                        tags.append(c_tag)
                        i = i + 1
                    num = num + m - 1
                    c_preds = [c_MFR[c_tag][1]]


                # list of entries in MFR's first "column"
                stems = [row[0] for row in c_MFR]

                # checks that all c_preds are in c_MFR
                if not set(c_preds).difference(set(stems)):
                    if verbose:
                        print("all predecessors are in current MFR")
                    # same as line 35
                    if c_tag == len(c_MFR) - 1:
                        flag = True
                        if verbose:
                            print("MFR finished")
                    else:
                        c_tag = c_tag + 1

                # appends new rows to current partial MFR
                else:
                    for v in c_preds:
                        temp2 = net[v]
                        if verbose:
                            print("preds of preds:", temp2)
                        if set(temp2).intersection(set(redundant)):
                            if graph.vs[v]["composite"]:
                                if verbose:
                                    print("ERROR: node can't be activated")
                                discard.append(c_MFR)
                                flag = True
                        else:
                            c_MFR.append([v, temp2])
                    c_tag = c_tag + 1
                    if verbose:
                        print("new partial MFR:", c_MFR)

        pointer = pointer + 1

        # list of entries in MFRs second 'column'
        stalks = [row[1] for row in c_MFR]
        # checks for discard and adds 'extraneous' MFRs to 'discard' list
        if not [] in stalks:
            discard.append(c_MFR)
        if verbose:
            print("discard:", discard)

    # removes "extra" MFRs, those that result from discard in graph and non-
    # activated nodes
    final_MFRs = []
    for mfr in all_MFRs:
        if not mfr in discard:
            final_MFRs.append(mfr)

    for mfr in final_MFRs:
        # removes unecessary "last" row of mfr
        for item in mfr:
            if item == [0,[]]:
                mfr.remove(item)
        # reverses order of everything (since alg is bottom-up)
        mfr.reverse()
        for item in mfr:
            item.reverse()
        # flattens list
        for item in mfr:
            if type(item[0]) is list:
                for i in item[0]:
                    mfr.insert(mfr.index(item) + 1, [i, item[1]])
                mfr.remove(item)

    # translates expanded vertices to original
    #contracted_MFRs = []
    #for mfr in final_MFRs:
        #new_mfr = []
        #if verbose:
            #print("old mfr:", mfr)
        #for edge in mfr:
            #if '~' in (graph.vs[edge[0]]["name"] or graph.vs[edge[1]]["name"]):
                #print("inhibitory edge:", edge)
            #if graph.vs[edge[0]]["composite"]:
                #for e in mfr:
                    #if e[1] == edge[0]:
                    #    new_mfr.append([e[0], edge[1]])
            #elif graph.vs[edge[1]]["composite"]:
            #    pass
            #else:
            #    new_mfr.append(edge)
        #contracted_MFRs.append(new_mfr)
        #if verbose:
            #print("new mfr:", new_mfr)

    # output options
    if verbose:
        print("Number of MFRs:", len(final_MFRs), "\n")

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
                id.append(graph.get_eid(chunk[0], chunk[1]))
                id.sort()
            ids.append(id)
        if verbose:
            for id in ids:
                print(ind, ":", id, "\n")
                ind += 1
        return [ids, len(ids)]
