from igraph import Graph, plot
from sympy.logic.boolalg import to_dnf

def updates(graph, synergy = [], inhibition = [], verbose = 0):
    """
    Given a graph and synergy/inhibition edge values, return the booleans
    update table of the graph

    Uses *python-igraph*:
    http://igraph.org/python/

    Parameters:
    graph  -- *igraph* Graph object
    synergy -- list of synergy values of the edge sequence
    inhibition -- list of binary inhibition values of the edge sequence
    verbose -- option to print update table

    """
    # initializes update table
    updatetable = graph.get_adjlist(mode = 'in')
    for l in updatetable:
        l.clear()
    edgelist = graph.get_edgelist()

    # keeps track of inhibitory edges
    inhibs = []
    for ind, val in enumerate(inhibition):
        if val:
            inhibs.append(edgelist[ind])

    # keeps track of synergies
    i=1
    indices = []
    while i <= max(synergy):
        indices.append(
        [syn for syn,val in enumerate(synergy) if val==i]
        )
        i += 1
    synergies = []
    for ind in indices:
        syn = [edgelist[i] for i in ind]
        synergies.append(syn)

    #converts synergy and inhibition data to table entries
    #synergy is checked first, then inhibition if applicable
    for group in synergies:
        predlist = []
        for e in group:
            if e in inhibs:
                negpred = '~{}'.format(graph.vs["name"][e[0]])
                predlist.append(negpred)

            else:
                pred = '{}'.format(graph.vs["name"][e[0]])
                predlist.append(pred)
        predstring = '({})'.format("&".join(predlist))
        updatetable[e[1]].append(predstring)

    #remaining edges
    or_edges = list(set(edgelist)-
    set([edge for group in synergies for edge in group]))

    for edge in or_edges:
        # inhibitory edges also checked for synergy to not double count
        if edge in inhibs:
            updatetable[edge[1]].append(
            '~{}'.format(graph.vs["name"][edge[0]])
            )

        else:
            updatetable[edge[1]].append(
            '{}'.format(graph.vs["name"][edge[0]])
            )

    # flattens and standardizes table entries
    for entry in updatetable:
        # first entry becomes empty string
        if not entry:
            updatetable[updatetable.index(entry)] = ""
        else:
            final_string = '{}'.format("|".join(entry))
            updatetable[updatetable.index(entry)] = final_string

    #computes logical negations for inhibitory nodes
    logical_negations = [[], []]
    for expression in updatetable:
        if '~' in expression:
            logical_negations[0].append(
            "~{}".format(graph.vs["name"][updatetable.index(expression)])
            )
            negation = str(to_dnf("~({})".format(expression))).replace(" ", "")
            logical_negations[1].append(negation)

    # entry table finalized with node indices
    updatetable = [
    graph.vs["name"]+logical_negations[0],
    updatetable+logical_negations[1]
    ]

    #option to see the table displayed
    if verbose:
        for entry in updatetable[0]:
            print(entry, "=", updatetable[1][updatetable[0].index(entry)])

    return updatetable

def expand(graph, table, verbose = 0):
    """
    Given a graph and an update table, return the expanded graph with
    negatory and composite nodes

    Uses *python-igraph* and *sympy*:
    http://igraph.org/python/
    http://www.sympy.org/en/index.html

    Parameters:
    graph  -- *igraph* Graph object
    table -- 2 by n boolean update table for the graph with n nodes
    verbose -- boolean denoting whether expanded graph will be printed and
    plotted

    """

    #starts building expanded graph based on update table
    edgelist = graph.get_edgelist()
    startcount = graph.vcount()
    names = graph.vs["name"]

    #adds NOT nodes to match inhibition
    if "inhibition" in graph.es.attributes():
        for source in table[0]:
            if not '~' in source:
                n1 = "~{}".format(source)
                names.append(n1)

    #adds AND nodes to match synergy
    for i in range("".join(table[1]).count('(')):
        n2 = "c{}".format(i+1)
        names.append(n2)

    names = list(dict.fromkeys(names))


    compcount = "".join(table[1]).count('(')
    edgelist = []
    group_counter = 0
    # adds edges to the new graph
    for entry in table[0]:
        for node in table[1][table[0].index(entry)].replace('(', '')\
        .replace(')', '').split("|"):

            # if AND node, make composite node
            if '&' in node:
                group_counter += 1
                # deletes previous synergistic edges
                for syn in node.split('&'):
                    edgelist.append(
                    (names.index(syn),
                    names.index("c{}".format(group_counter)))
                    )

                edgelist.append(
                (names.index("c{}".format(group_counter)), names.index(entry))
                )

            elif not node == '':
                edgelist.append((names.index(node), names.index(entry)))

    # finalizes the graph
    edgelist = list(dict.fromkeys(edgelist))
    exp_graph = Graph(directed = True)
    exp_graph.add_vertices(len(names))
    exp_graph.add_edges(edgelist)
    #removes singleton nodes
    #isolated = []
    #for node in names:
        #if exp_graph.neighbors(names.index(node)) == []:
            #isolated.append(names.index(node))
    #exp_graph.delete_vertices(isolated)
    #for index in isolated:
        #names.remove(names[index])
    exp_graph.vs["name"] = names
    exp_graph.vs["label"] = names
    #[ind for ind, val in enumerate(exp_graph.vs["name"])]
    exp_graph.vs["composite"] = [0 * graph.vcount()]
    for i in range((len(names)-compcount), len(names)):
        exp_graph.vs[i]["composite"] = 1

    if verbose:
        print(exp_graph)
        plot(exp_graph, vertex_size = 30,
        edge_arrow_size = 0.75, vertex_color = "white", bbox=(0, 0, 600, 600))
    return exp_graph
