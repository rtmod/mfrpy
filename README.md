# mfrpy: Package Initialization

### Import the module:

```py
from mfrpy import alg3
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


## Finding the Minimal Functional Routes:

Call the get_mfrs() method:

```py
alg3.get_mfrs(acyclic, 0, 9, True, "el")
```

or

```py
alg3.get_mfrs(cyclic, 0, 7, True, "el")
```


The parameters of the get_mfrs method are as follows:

```py
get_mfrs(

graph -- *igraph* Graph object, 

source node index -- int, 

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

# Encoding your graph's dependent edges

### Add the synergy attribute to the edge sequence of your igraph Graph object:

acyclic example

```py
acyclic.es["synergy"] = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0]
```

Here edges 4 and 5 are dependent on one another and so are edges 10 and 13. 
However, edges 4 and 10, for example, are independent.

0 represents no synergy (regular edge)

Edges with the same value for the synergy attribute are dependent on one another



