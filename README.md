# nxnk
A networkx-like wrapper for the NetworKit library

```nxnk``` aims at providing a drop-in replacement for networkx Graph and DiGraph classes, whenever node and edge attributes are not necessary.

NetworKit (https://github.com/kit-parco/networkit) is a python library focusing on high performance graph analysis by means of a finely tuned C++ backend, whereas NetworkX (https://github.com/networkx/networkx) is a widely used python-only library for constructing, manipulating and analyzing graphs.

With its focus on performance, NetworKit offers an ideal library for the analysis of large graphs.

This library, *nxnk*, is an attempt at easing the creation and editing of graphs like NetworkX while maintaining the performance-enhanced algorithms of NetworKit.

In creating and editing graphs, the performance of *nxnk* is comparable (slightly better: 10-50%) to that of NetworkX.

You could thin of ```nxnk``` as providing a mapping between your graph nodes (any hashable object) and NetworKit's internal node representation (an integer), by using a networkx-like interface.

This is an alpha release, subject to change and quite incomplete. At present, only ```Graph``` and ```DiGraph``` are supported, with only some bridge functions to access NetworKit algorithm implementations. To access the latter, use the ```self.nkG```, which is an instance of a NetworKit ```graph.Graph```, and translate between user-defined nodes and NetworKit-defined nodes (the "knodes") using the dictionaries ```nodes``` and ```knodes``` in either ```Graph``` or ```DiGraph```, or use the convenience methods ```to_user_nodes``` and ```to_networkit_nodes```. Otherwise, all presently existing methods operate exclusively in user-defined node IDs, taking as argument and returning only user-defined node IDs (with the exception of ```to_networkit_nodes```).

```nxnk``` targets python 3, and recommends python 3.6+.

## Differences between nxnk and NetworkX

1. NetworkX Graph and DiGraph classes offer a number of methods suffixed with "_iter" (e.g. ```networkx.Graph.edges_iter```), which are implemented as generators (with the ```yield``` keyword; see: https://networkx.github.io/documentation/development/_modules/networkx/classes/graph.html#Graph), with the "_iter"-free method (e.g. ```networkx.Graph.edges```) calling ```list``` on the return value of the twin "_iter" method.
   In ```nxnk```, these additional "_iter" methods are merely provided by compatibility with networkx and marked as deprecated. By design, the proper methods are implemented directly as generators. In this aspect, nxnk follows a similar shift from python 2 to python 3, in that e.g. the ```range``` function went from returning a list to merely promising to generate one on the fly, and removed from python 3 all the "_iter"-suffixed methods that had been added to python 2 for performance reasons.

2. ```nxnk``` does not store a dictionary of properties for every node and for every edge, unlike NetworkX. All ```nxnk``` provides is the means to store a floating-point value as edge weight, mirroring the capabilities of the ```networkit.Graph```. Note that you will have to initialize ```nxnk.Graph``` or ```nxnk.DiGraph``` with ```weighted=True``` (the default) for graph edges to be able to hold weights other than 1.0.
   Deriving from this fundamental feature, ```nxnk``` does not provide any means to store edge or node property maps (networkx stores a dictionary for every node and edge, even an empty one when not providing any properties), and therefore, all methods that in networkx take attribute maps do not do so in ```nxnk```. Fortunately, these are always provided as optional arguments in networkx, and therefore, if you code does not use them, ```nxnk``` will work as a drop-in replacement.

3. Networkx graph classes offer the method ```degree``` which works for both a single node, a list of nodes, or all nodes, returning different data types depending on the argument. In ```nxnk```, functions always return the same data type (or None), and therefore ```degree``` is limited to returning the degree of a single node. Use ```degrees``` for an iterable of the degree of all nodes, and map ```degree``` to an iterable of a subset of nodes when wanting the degree of a subset of nodes.


## Using nxnk Graph and DiGraph with NetworkX functions (networkx interop)

Given that ```nxnk``` Graph and DiGraph classes offer the same function interface as their homonimous classes in NetworkX, most of the NetworkX library can operate correctly with ```nxnk``` versions of Graph and DiGraph.

For cases where NetworkX library functions expect lists instead of generators, call the method ```nx_adapter()``` in either Graph or DiGraph which will produce an editable view (```NXGraph``` or ```NXDiGraph```) with methods that behave like those of NetworkX (e.g. returning a list instead of a generator).

