# Introduction
mfrpy is a Python package for finding the minimal functional routes of signal transduction networks. The package builds on work done at Pennsylvania State University by Réka Albert, Rui-Sheng Wang, and others. This is part of the *rtmod* pipeline for calculating the modulus of a family of routes.  This is done in two parts - first, the graph is expanded by the *update_expand.py* method. Our approach sees expansion mediated by an update table, simplifying computations in lieu of graph-theoretic expansion "by hand". For users interested in expansion, see [1]. Secondly, the minimal functional routes, minimal subgraphs of the expanded graph, are found using *sgmfr.py*, an algorithm adopted into Python from [2]. After computation, the minimal routes are returned in terms of original graph vertices and edges to the user. The following is meant to be an introduction to the package for novel users. For a more thorough explanation, refer to *rtmod tutorial.ipynb*. For more information on signal transduction networks in general, see [3].

# mfrpy: Package Initialization

### Import the module:

```py
from mfrpy import sgmfr
```

### Import the example graphs:

```py
from mfrpy.examplegraphs import igraph_graph
```

### Initialize the example graphs:

acyclic example

```py
acyclic = igraph_graph.dag
```

cyclic example

```py
cyclic = igraph_graph.dcg
```

user can also import their own graphs by standard igraph commands. For GraphML files

```py
myGraph = Graph.Read_GraphML("myGraph.xml")
myGraph.vs["name"] = myGraph.vs["id"]
```

## Finding the Minimal Functional Routes:

Call the get_mfrs() method:

```py
sgmfr.get_mfrs(acyclic, [0], 9, True, "el")
```

or

```py
sgmfr.get_mfrs(cyclic, [0], 7, True, "el")
```


The parameters of the get_mfrs method are as follows:

```py
get_mfrs(

graph -- *igraph* Graph object, 

source node indices -- list, 

target node index -- int, 

option to display mfrs -- defaults to False,

output option -- defaults to "es"

)
```


Supported output options:

```py
"em" -- returns edge matrices

"el" -- returns edge lists

"es" -- returns edge sequence indices
```

## Encoding your graph's dependent edges

### Add the synergy attribute to the edge sequence of your igraph Graph object:

acyclic example

```py
acyclic.es["synergy"] = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0]
```

Here edges 4 and 5 are dependent on one another and so are edges 10 and 13. 
However, edges 4 and 10, for example, are independent.

0 represents no synergy (regular edge)

Edges with the same value for the synergy attribute are dependent on one another

To do the same for **inhibition**, 

```py
acyclic.es["inhibition"] = [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
```

Where 1 indicates an inhibitory edge while 0 indicates activation


## References

[1] Wang and Albert: **Elementary signaling modes predict the essentiality of signal transduction network components.** *BMC Systems Biology* 2011 **5**:44

[2] Wang et al.: **Minimal functional routes in directed graphs with dependent edges**. *International Transactions in Operational Research* 2013

[3] Albert and Robeva: **Signaling Networks : Asynchronous Boolean Models**. *Algebraic and Discrete Mathematical Methods for Modern Biology.* Elsevier, 2015. pp. 65-91

