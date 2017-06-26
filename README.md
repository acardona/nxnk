# nxnk
A networkx-like wrapper for the NetworKit library

NetworKit (https://github.com/kit-parco/networkit) is a python library focusing on high performance graph analysis by means of a finely tuned C++ backend, whereas NetworkX (https://github.com/networkx/networkx) is a widely used python-only library for constructing, manipulating and analyzing graphs.

With its focus on performance, NetworKit offers an ideal library for the analysis of large graphs.

This library, *nxnk*, is an attempt at easing the creation and editing of graphs like NetworkX while maintaining the performance-enhanced algorithms of NetworKit.

In creating and editing graphs, the performance of *nxnk* is comparable (slightly better: 10-30%) to that of NetworkX.

This is an alpha release, subject to change and quite incomplete. At present, only ```Graph``` and ```DiGraph``` are supported, and they lack bridge functions to access NetworKit algorithm implementations. To access the latter, use the ```self.nkG```, which is an instance of a NetworKit ```graph.Graph```, and translate between user-defined nodes and NetworKit-defined nodes (the "knodes") using the dictionaries ```nodes``` and ```knodes``` in either ```Graph``` or ```DiGraph```, or use the convenience methods ```to_user_nodes``` and ```to_networkit_nodes```. Otherwise, all presently existing methods operate exclusively in user-defined node IDs, taking as argument and returning only user-defined node IDs (with the exception of ```to_networkit_nodes```).

```nxnk``` targets python 3, and recommends python 3.6+.

## Differences between nxnk and NetworkX

1. NetworkX Graph and DiGraph classes offer a number of methods suffixed with "_iter" (e.g. ```networkx.Graph.edges_iter```), which are implemented as generators (with the ```yield``` keyword; see: https://networkx.github.io/documentation/development/_modules/networkx/classes/graph.html#Graph), with the "_iter"-free method (e.g. ```networkx.Graph.edges```) calling ```list``` on the return value of the twin "_iter" method.

In ```nxnk```, these additional "_iter" methods will not be implemented, with the proper methods being implemented directly as generators.

2. ```nxnk``` does not store a dictionary of properties for every node and for every edge, unlike NetworkX which does so. All ```nxnk``` provides is the means to store a floating-point value as edge weight, mirroring the capabilities of the ```networkit.Graph```. Note that you will have to initialize ```nxnk.Graph``` or ```nxnk.DiGraph``` with ```weighted=True``` (the default) for graph edges to be able to hold weights other than 1.0.
