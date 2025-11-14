from igraph import *

exp_dcg = Graph(directed = True) # immitates expanded dcg graph
exp_dcg.add_vertices(10)
# edges (1, 5) & (2, 5) and (0, 2) & (4, 2) in dcg have synergy
exp_dcg.add_edges([
(0,1), (0,3), (3,4), (5,4), (4,6),
(6,5), (5,7), (6,7), (0, 8), (4, 8), (8, 2), (1, 9), (2, 9), (9, 5)
])
exp_dcg.vs["name"] = ["I", "A", "B", "C", "D", "E", "F", "O", "c1", "c2"]
exp_dcg.composite_nodes = [8, 9] # nodes 8 and 9 are composite nodes

def get_mfrs(graph, source, target, mode = "es"):

    print("Initializing")
    print('*' * 124)
    # initialization
    pointer = 0
    num = 1
    # tags is an array of integers, python starts counting from 0
    tags = [0]
    flag = False
    cycles = []


    net = graph.get_adjlist(mode='in')
    all_MFRs = [[[target, net[target]]]]
    print(graph)
    print('*' * 124)

    # while some partial MFRs remain
    while pointer < num:
        print("pointer:", pointer)
        print("Number of partial MFRs:", num)
        flag = False
        c_MFR = all_MFRs[pointer]
        # print("current MFR:", c_MFR)
        c_tag = tags[pointer]
        print("current tag:", c_tag)
        # while the current MFR is incomplete
        while not flag:
            c_node = c_MFR[c_tag][0]
            print("current node:", c_node)
            # c_preds is a list of integers
            c_preds = c_MFR[c_tag][1]
            print("predecessors:", c_preds)

            # if no predecessors remain
            # python uses implicit booleans for lists
            if not c_preds:
                if c_tag == len(c_MFR) - 1:
                    flag = True
                else:
                    c_tag = c_tag + 1

            else:
                # if True:
                if not c_node in graph.composite_nodes:
                # placeholder;
                # actually need to check that c_node is not a composite node
                    m = len(c_preds)
                    c_MFR[c_tag][1] = c_preds[0]

                    # allots memory to new partial MFRs
                    i = 0
                    while i < m - 1:
                        temp1 = [li[:] for li in c_MFR]
                        temp1[c_tag][1] = [c_preds[i + 1]]
                        # print("c_MFR:", c_MFR)
                        # print("temp1:", temp1)
                        # current MFR is replaced by first copy
                        all_MFRs.append(temp1)
                        tags.append(c_tag)
                        i = i + 1
                    num = num + m - 1
                    c_preds = [c_MFR[c_tag][1]]
                    print("***new partial MFRs created***")
                    print("Number of partial MFRs:", num)
                else:
                    print("\ncurrent node is a composite node\n")

                # returns list of entries in MFR's first "column"
                stems = [row[0] for row in c_MFR]
                print("stems:", stems)

                # checks that all c_preds are in c_MFR
                if not set(c_preds).difference(set(stems)):
                    # same as line 35
                    print("all predecessors are in the current MFR")
                    if c_tag == len(c_MFR) - 1:
                        flag = True
                        print("flag drops")
                    else:
                        c_tag = c_tag + 1
                # appends new rows to current partial MFR
                else:
                    for v in c_preds:
                        temp2 = net[v]
                        c_MFR.append([v, temp2])
                    print("+++new rows appended to current MFR+++")
                    c_tag = c_tag + 1

        pointer = pointer + 1

        stalks = [row[1] for row in c_MFR]
        print("stalks:", stalks)
        if not [] in stalks:
            print("cycle deteceted!")
            cycles.append(c_MFR)

        print("Completed MFR:", c_MFR)
        print("Cycles:")
        for cycle in cycles:
            print(cycle)
        print("Number of cycles:", len(cycles))
        print('*' * 124)
    print("all MFRs:")
    for mfr in all_MFRs:
        print(mfr)

    print('*' * 124)
    print("Final MFRs:")
    print('*' * 124)

    # removes "extra" MFRs, those that result from cycles in graph
    final_MFRs = []
    for mfr in all_MFRs:
        if not mfr in cycles:
            final_MFRs.append(mfr)

    for mfr in final_MFRs:
        # removes unnecessary "last" row of mfr
        for item in mfr:
            if item == [0,[]]:
                mfr.remove(item)
        # 'mode' argument is for how user wants mfrs to be displayed
        # reverses order of everything (since alg is bottom-up)
        mfr.reverse()
        for item in mfr:
            item.reverse()
        # flattens list
        # BUG FIX: Using .index() can fail if item not found, but in this context
        #          it should be safe since we're iterating over items in mfr
        #          However, using enumerate would be safer for future modifications
        for item in mfr:
            if type(item[0]) is list:
                for i in item[0]:
                    try:
                        mfr.insert(mfr.index(item) + 1, [i, item[1]])
                    except ValueError:
                        # Item not found, skip
                        pass
                mfr.remove(item)

    # output options
    if mode == "em": # "em" = edge matrix
        ind = 1
        for mfr in final_MFRs:
            print("\n", ind, ":")
            for chunk in mfr:
                print(chunk)
            ind += 1
    elif mode == "el": # "el" = edge list
        ind = 1
        for mfr in final_MFRs:
            print("\n", ind, ":", mfr)
            ind += 1
    elif mode == "es": # "es" = edge sequence ids
        ids = []
        ind = 1
        for mfr in final_MFRs:
            id = []
            for chunk in mfr:
                # BUG FIX: Same as Bug Fix #4 - Added error handling for missing edges
                try:
                    eid = graph.get_eid(chunk[0], chunk[1])
                    id.append(eid)
                except Exception:
                    # Edge doesn't exist in graph, skip it
                    print(f"Warning: Edge ({chunk[0]}, {chunk[1]}) not found in graph")
            ids.append(id)
        for id in ids:
            print(ind, ":", id, "\n")
        ind += 1

    print('*' * 124)
    print("Number of MFRs:", len(final_MFRs))
    print('*' * 124)

get_mfrs(exp_dcg, 0, 7, "el")
