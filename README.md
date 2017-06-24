# nxnk
A networkx-like wrapper for the NetworKit library

NetworKit (https://github.com/kit-parco/networkit) is a python library focusing on high performance graph analysis by means of a finely tuned C++ backend, whereas NetworkX (https://github.com/networkx/networkx) is a widely used python-only library for constructing, manipulating and analyzing graphs.

With its focus on performance, NetworKit offers an ideal library for the analysis of large graphs.

This library, *nxnk*, is an attempt at easing the creation and editing of graphs like NetworkX while maintaining the performance-enhanced algorithms of NetworKit.

In creating and editing graphs, the performance of *nxnk* is comparable (slightly better) to that of NetworkX.

This is an alpha release, subject to change and quite incomplete. At present, only ```Graph``` and ```DiGraph``` are supported, and they lack bridge functions to access NetworKit algorithm implementations. To access the latter, use the ```self.nkG```, which is an instance of a NetworKit ```graph.Graph```, and translate between user-defined nodes and NetworKit-defined nodes (the "knodes") using the dictionaries ```nodes``` and ```knodes``` in either ```Graph``` or ```DiGraph```, or use the convenience methods ```to_user_nodes``` and ```to_networkit_nodes```.
