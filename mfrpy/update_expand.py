from igraph import *
from sympy.logic.boolalg import to_dnf

def updates(graph, synergy = [], inhibition = []):
    """
    Given a graph and synergy/inhibition edge values, return the booleans
    update table of the graph

    Uses *python-igraph*:
    http://igraph.org/python/

    Parameters:
    graph  -- *igraph* Graph object
    synergy -- list of synergy values of the edge sequence
    inhibition -- list of binary inhibition values of the edge sequence

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

    # converts synergy and inhibition data to table entries
    synthrshld = 1
    for edge in edgelist:

        #synergy is checked first, then inhibition if applicable
        if synergy[edgelist.index(edge)] == synthrshld:
            for e in synergies[1-synthrshld]:
                if e in inhibs:
                    updatetable[edge[1]].append(
                    ['~{}'.format(graph.vs["name"][ed[0]]) \
                    for ed in synergies[1-synthrshld]]
                    )
                    synthrshld += 1
                    break
                else:
                    updatetable[edge[1]].append(['{}'.format(
                    graph.vs["name"][ed[0]]) for ed in synergies[1-synthrshld]]
                    )
                    synthrshld += 1
                    break
            continue

        # inhibitory edges also checked for synergy to not double count
        if edge in inhibs:
            if synergy[edgelist.index(edge)]:
                pass
            else:
                updatetable[edge[1]].append(
                '~{}'.format(graph.vs["name"][edge[0]])
                )
        else:
            updatetable[edge[1]].append(
            '{}'.format(graph.vs["name"][edge[0]])
            )

    # flattens and standardizes table entries
    # first entry becomes None data type
    for entry in updatetable:
        for block in entry:
            if isinstance(block, str):
                pass
            else:
                updatetable[updatetable.index(entry)].append("&".join(block))
                updatetable[updatetable.index(entry)].remove(block)
                break
        updatetable[updatetable.index(entry)] = "|".join(entry)

    # entry table finalized with node indices
    updatetable = [[count for count, value in enumerate(updatetable)],
    updatetable]

    return updatetable



def expand(graph, table):
    """
    Given a graph and an update table, return the expanded graph with
    negatory and composite nodes

    Uses *python-igraph* and *sympy*:
    http://igraph.org/python/
    http://www.sympy.org/en/index.html

    Parameters:
    graph  -- *igraph* Graph object
    table -- 2 by n boolean update table for the graph with n nodes

    """

    #starts building expanded graph based on update table
    edgelist = graph.get_edgelist()
    startcount = graph.vcount()
    names = graph.vs["name"]

    # keeps track of inhibitory edges
    inhibs = []
    if 'inhibition' in graph.es.attributes():
        for ind, val in enumerate(graph.es["inhibition"]):
            if val:
                inhibs.append(edgelist[ind])

    #adds NOT nodes to match inhibition
    for edge in inhibs:
        for node in edge:
            if "~{}".format(graph.vs["name"][node]) not in names:
                graph.add_vertices(1)
                name = "~{}".format(graph.vs["name"][node])
                names.append(name)
    tempcount = graph.vcount()
    graph.vs["name"] = names

    # initializes variables for graph expansion
    counter = 0
    for i in inhibs:
        edgelist.remove(i)
    lnegs = [[],[]]

    # expands the graph
    compcount = 0
    for index in table[0]:
        for node in table[1][index].split("|"):

            # if NOT node, take the logical negation and add/remove edges
            if '~' in node:
                logneg = to_dnf("~({})".format(node))
                lnegs[0].append(to_dnf("~({})".format(graph.vs["name"]
                [table[0][index]])))
                lnegs[1].append(logneg)
                temp = node
                if '&' in node:
                    temp = node.split("&")
                if isinstance(temp, str):
                    edgelist.append((names.index(temp), index))
                else:
                    for sub in temp:
                        edgelist.append((names.index(sub), index))

            # if AND node, make composite node
            if '&' in node:
                counter += 1
                # adds new vertices
                graph.add_vertices(1)

                # deletes previous synergistic edges
                for syn in node.split('&'):
                    edgelist.remove((names.index(syn), index))

                # gives names to new composite nodes
                name = "c{}".format(counter)
                compcount += 1
                names.append(name)
                edgelist.append((tempcount + counter - 1, index))
                for syn in node.split('&'):
                    edgelist.append((names.index(syn), tempcount + counter - 1))

            elif not node == '':
                edgelist.append((names.index(node), index))

    # expands the graph for logical negations
    for node in lnegs[1]:
        source = lnegs[0][lnegs[1].index(node)]

        # if AND node, make composite node
        if '&' in str(node):
            counter += 1
            # adds new vertices
            graph.add_vertices(1)
            # gives names to new composite nodes
            name = "c{}".format(counter)
            compcount += 1
            names.append(name)
            edgelist.append((tempcount + counter - 1, names.index(str(source))))
            for syn in node.replace('(', '').replace(')', '').replace(' ',
             '').split('&'):
                edgelist.append((names.index(syn), tempcount + counter - 1))

        # if NOT node, take the logical negation and add/remove edges
        if '|' in str(node):
            for x in str(node).replace('(', '').replace(')', '').replace(' ',
             '').split("|"):
                edgelist.append((names.index(str(x)), names.index(str(source))))

        else:
            edgelist.append((names.index(str(node)), names.index(str(source))))

    edgelist = list(dict.fromkeys(edgelist))
    print(edgelist)

    # finalizes the graph
    exp_graph = Graph(directed = True)
    exp_graph.add_vertices(graph.vcount())
    exp_graph.add_edges(edgelist)
    exp_graph.vs["name"] = names
    exp_graph.vs["composite"] = [0 * graph.vcount()]
    for i in range(graph.vcount()-compcount, graph.vcount()):
        exp_graph.vs[i]["composite"] = 1

    return exp_graph
