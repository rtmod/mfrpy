from igraph import Graph, plot
from tabulate import tabulate
from sympy.logic.boolalg import to_dnf

def prime(graph):
    """
    For a given graph, returns the edgelist with correct synergies as well as
    list of inhibitory edges. Necessary for graphs with multiple edges and
    synergies.

    Parameters:
    graph  -- *igraph* Graph object with synergy and inhibition attributes

    """

    # Initializes lists
    inhibs = []
    #try:
    #    for ind, val in enumerate(graph.es["inhibition"]):
    #        if val:
    #            inhibs.append(graph.get_edgelist()[ind])
    #except KeyError:
    #    pass
    try:
        synergy = graph.es["synergy"]
    except KeyError:
        synergy = [ind for ind, val in enumerate(graph.get_edgelist())]

    # Gives every edge a nonzero synergy value
    newval = max(synergy) + 1
    for value in synergy:
        if value == 0:
            synergy[synergy.index(value)] = newval
            newval += 1

    # Keeps track of synergies
    tochange = [list(dict.fromkeys(synergy)),[]]
    for num in tochange[0]:
        dependentedges = []
        adder = 0
        for syn in synergy:
            if num == syn:
                dependentedges.append(
                graph.get_edgelist()[
                (([0] * adder) + synergy[adder:]).index(syn)
                ])
                adder = (([0] * adder) + synergy[adder:]).index(syn) + 1
        tochange[1].append(dependentedges)

    changeto = involution(tochange)

    # Creates new edgelist array with edge and synergy lists
    edgelist = [[],[]]
    for e in changeto[0]:
        for s in changeto[1][changeto[0].index(e)]:
            edgelist[0].append(e)
            edgelist[1].append(s)

    #table = [["id", "link", "syn", "inhibition"]]
    #i = 0
    #while i < len(edgelist[0]):
    #    edge = edgelist[0][i]
    #    table.append([i, graph.vs[edge[0]]["name"]+'\u2192'+
    #    graph.vs[edge[1]]["name"],
    #    int(edgelist[1][i]),
    #    bool(0)])
    #    i+=1
    #print(tabulate(table, headers='firstrow', tablefmt = "github"))

    return [edgelist, inhibs]

def updates(graph, synergy = [], inhibition = [], verbose = 0):
    """
    Given a graph and synergy/inhibition edge values, return the boolean
    update table of the graph

    Uses *python-igraph*:
    http://igraph.org/python/

    Parameters:
    graph  -- *igraph* Graph object
    synergy -- list of synergy values of the edge sequence
    inhibition -- list of binary inhibition values of the edge sequence
    verbose -- option to print update table

    """

    # Initializes update table
    updatetable = graph.get_adjlist(mode = 'in')
    for l in updatetable:
        l.clear()
    edgelist = prime(graph)[0]
    # Extracts inhibitory edges
    inhibs = prime(graph)[1]

    # Converts synergy and inhibition data to table entries
    i=1
    indices = []
    while i <= max(edgelist[1]):
        indices.append(
        [syn for syn, val in enumerate(edgelist[1]) if val==i]
        )
        i += 1
    synergies = []
    for ind in indices:
        syn = [edgelist[0][i] for i in ind]
        synergies.append(syn)

    # Synergy is checked first, then inhibition if applicable
    for group in synergies:
        predlist = []
        for e in group:
            if e in inhibs:
                negpred = '~{}'.format(graph.vs["name"][e[0]])
                predlist.append(negpred)
            else:
                pred = '{}'.format(graph.vs["name"][e[0]])
                predlist.append(pred)
        # For independent edges
        if len(predlist) == 1:
            predstring = predlist[0]
        else:
            predstring = '({})'.format("&".join(predlist))
        updatetable[e[1]].append(predstring)

    # Flattens and standardizes table entries
    for entry in updatetable:
        # First entry becomes empty string
        if not entry:
            updatetable[updatetable.index(entry)] = ""
        else:
            final_string = '{}'.format("|".join(entry))
            updatetable[updatetable.index(entry)] = final_string

    # Computes logical negations for inhibitory nodes
    logical_negations = [[], []]
    for expression in updatetable:
        if '~' in expression:
            logical_negations[0].append("~{}".format(
            graph.vs["name"][updatetable.index(expression)]
            ))
            negation = str(to_dnf("~({})".format(expression))).replace(" ", "")
            logical_negations[1].append(negation)

    # Entry table finalized with node indices
    updatetable = [
    graph.vs["name"] + logical_negations[0],
    updatetable + logical_negations[1]
    ]

    # Option to see the table displayed
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

    # Starts building expanded graph based on update table
    startcount = graph.vcount()
    names = graph.vs["name"]

    # Adds NOT nodes to match inhibition
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
    # Adds edges to the new graph
    for entry in table[0]:
        for node in table[1][table[0].index(entry)].replace('(', '')\
        .replace(')', '').split("|"):
            # If AND node, make composite node
            if '&' in node:
                group_counter += 1
                # Deletes previous synergistic edges
                for syn in node.split('&'):
                    edgelist.append(
                    (names.index(syn),
                    names.index("c{}".format(group_counter)))
                    )

                edgelist.append((
                names.index("c{}".format(group_counter)),
                names.index(entry)
                ))

            elif not node == '':
                edgelist.append((names.index(node), names.index(entry)))

    # Finalizes the graph
    edgelist = list(dict.fromkeys(edgelist))
    exp_graph = Graph(directed = True)
    exp_graph.add_vertices(len(names))
    exp_graph.add_edges(edgelist)
    exp_graph.vs["name"] = names
    exp_graph.vs["label"] = names
    exp_graph.vs["composite"] = [0 * graph.vcount()]
    for i in range((len(names)-compcount), len(names)):
        exp_graph.vs[i]["composite"] = 1

    # Removes isolated nodes
    #nicergraph = exp_graph
    #isolated = []
    #for node in names:
    #    if exp_graph.neighbors(names.index(node)) == []:
    #        isolated.append(names.index(node))
    #nicergraph.delete_vertices(isolated)

    if verbose:
        print(exp_graph)
        #plot(exp_graph, vertex_size = 30,
        #edge_arrow_size = 0.75, vertex_color = "white", bbox=(0, 0, 600, 600))

    return exp_graph


def involution(array):
    """
    returns the involution of an array -
    returns the original array if composed with itself
    resolves issue with multiple edges in STNs

    Parameters:
    array -- a list of edge lists and synergy values, in any order

    """

    # Initializes dictionary, separates array
    involved = {}
    unique = array[0]
    lists = array[1]
    shuffle = []

    # Making pairs of data from array
    for sub in lists:
        for thing in sub:
            shuffle.append([thing, unique[lists.index(sub)]])
    keys = list(set([pair[0] for pair in shuffle]))
    couples = [pair[1] for pair in shuffle]

    # Rearranging and recombining pairs
    for key in keys:
        value = []
        for pair in shuffle:
            if key == pair[0]:
                value.append(couples[shuffle.index(pair)])
        involved[key] = list(set(value))
    new_array = [list(involved.keys()), list(involved.values())]

    return new_array

dcg = Graph(directed = True) # directed cyclic graph, no composite nodes
dcg.add_vertices(8)
dcg.add_edges([
    (0,1), (0,2), (0,3), (3,4),
    (4,2), (2,5), (1,5), (5,4),
    (4,6), (6,5), (5,7), (6,7)
    ])
dcg.vs["name"] = ["i", "a", "b", "c", "d", "e", "f", "o"]
dcg.es["synergy"] = [0, 1, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0]

manysyns = Graph(directed = True)
manysyns.add_vertices(5)
manysyns.add_edges([
    (0,1), (0,2), (0,3), (1,4),
    (2,4), (2,4), (3,4)
    ])
manysyns.vs["name"] = ["a", "b", "c", "d", "e"]
manysyns.es["synergy"] = [0, 0, 0, 1, 1, 2, 2]

tab = updates(dcg, dcg.es["synergy"])

expand(dcg, tab)
