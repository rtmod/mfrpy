from igraph import *

def get_mfrs(graph, source, target, verbose = False, mode = "es"):

    # initialization
    pointer = 0
    num = 1
    # tags is an array of integers, python starts counting from 0
    tags = [0]
    flag = False
    cycles = []
    net = graph.get_adjlist(mode='in')
    all_MFRs = [[[target, net[target]]]]

    # while some partial MFRs remain
    while pointer < num:
        flag = False
        c_MFR = all_MFRs[pointer]
        # print("current MFR:", c_MFR)
        c_tag = tags[pointer]
        # while the current MFR is incomplete
        while not flag:
            c_node = c_MFR[c_tag][0]
            # c_preds is a list of integers
            c_preds = c_MFR[c_tag][1]

            # if no predecessors remain
            # python uses implicit booleans for lists
            if not c_preds:
                if c_tag == len(c_MFR) - 1:
                    flag = True
                else:
                    c_tag = c_tag + 1

            else:
                # attempt to emulate expanded graph functionality
                if not c_node in graph.composite_nodes:
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

                # returns list of entries in MFR's first "column"
                stems = [row[0] for row in c_MFR]

                # checks that all c_preds are in c_MFR
                if not set(c_preds).difference(set(stems)):
                    # same as line 35
                    if c_tag == len(c_MFR) - 1:
                        flag = True
                    else:
                        c_tag = c_tag + 1
                # appends new rows to current partial MFR
                else:
                    for v in c_preds:
                        temp2 = net[v]
                        c_MFR.append([v, temp2])
                    c_tag = c_tag + 1

        pointer = pointer + 1

        # returns list of entries in MFRs second 'column'
        stalks = [row[1] for row in c_MFR]
        # checks for cycles and adds 'extraneous' MFRs to 'cycles' list
        if not [] in stalks:
            cycles.append(c_MFR)

    # removes "extra" MFRs, those that result from cycles in graph
    final_MFRs = []
    for mfr in all_MFRs:
        if not mfr in cycles:
            final_MFRs.append(mfr)

    for mfr in final_MFRs:
        # removes unecessary "last" row of mfr
        for item in mfr:
            if item == [0,[]]:
                mfr.remove(item)
        # 'mode' argument is for how user wants mfrs to be displayed
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

    # output options
    if verbose:
        print("Number of MFRs:", len(final_MFRs), "\n")
        print("Final MFRs:")
    if mode == "em": # "em" = edge matrix
        ind = 1
        for mfr in final_MFRs:
            if verbose:
                print("\n", ind, ":")
                for chunk in mfr:
                    print(chunk)
            ind += 1
        return([final_MFRs, len(final_MFRs)])
    elif mode == "el": # "el" = edge list
        ind = 1
        for mfr in final_MFRs:
            if verbose:
                print("\n", ind, ":", mfr)
            ind += 1
        return([final_MFRs, len(final_MFRs)])
    elif mode == "es": # "es" = edge sequence ids
        ids = []
        ind = 1
        for mfr in final_MFRs:
            id = []
            for chunk in mfr:
                id.append(graph.get_eid(chunk[0], chunk[1]))
            ids.append(id)
        if verbose:
            for id in ids:
                print(ind, ":", id, "\n")
                ind += 1
        return([ids, len(ids)])
