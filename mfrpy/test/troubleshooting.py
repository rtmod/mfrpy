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

def get_mfrs(graph, source, target, mode = "em"):

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

    #output options
    ind = 1
    for mfr in final_MFRs:
        # removes unecessary "last" row of mfr
        modmfr = [chunk for chunk in mfr if chunk != [0,[]] ]
        # 'mode' argument is for how user wants mfrs to be displayed
        if mode == "em": # "em" = edge matrix
            print("\n", ind, ":")
            for item in modmfr[::-1]:
                print(item[::-1])
                #reverses order of everything (since alg is bottom-up)
        elif mode == "el": # "el" = edge list
            print(ind, ":", "\n")
        elif mode == "id": # "id" = edge ids
            print(ind, ":", "\n")
        ind += 1

    print('*' * 124)
    print("Number of MFRs:", len(final_MFRs))
    print('*' * 124)

get_mfrs(exp_dcg, 0, 7, "em")
