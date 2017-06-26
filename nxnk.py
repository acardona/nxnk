"""
This module provides networkx-like graph constructors and methods with a NetworKit backend.

Besides convenient, networkx-like functions, this wrapper class protects from
the fragility of NetworKit at the expense of performance when constructing the graph.

Unlike networkx, this networkx-like wrapper over NetworKit does not concern itself with
attributes other than weight.

By design, the iterable of user-defined nodes provided as argument to many methods is only ever read once. This enables consuming generators effectively.

Albert Cardona, 2017-06-23

"""

from networkit import graph
from itertools import chain
from collections import deque

class Graph:
    def __init__(self, directed=False, weighted=True):
        self.nkG = graph.Graph(weighted=weighted, directed=directed)
        # Map of user-defined nodes to NetworKit-defined node IDs
        self.nodes = {}
        # Map of NetworKit-defined node IDs vs user-defined nodes
        self.knodes = {}

    def to_user_nodes(self, knodes):
        """ Return the user-defined node corresponding to each given NetworKit node ID (a knode). """
        for knode in knodes:
            yield self.knodes[knode]

    def to_networkit_nodes(self, nodes):
        """ Return the NetworKit node ID (a knode) corresponding to each given user-defined node. """
        for node in nodes:
            yield self.nodes[node]

    def add_node(self, node):
        """ Adds the node and returns the NetworKit ID for the newly added node.
            If the node already existed, returns the existing NetworKit ID. """
        # If present, return it
        knode = self.nodes.get(node, None)
        if knode is None:
            knode = self.nkG.addNode()
            self.nodes[node] = knode
            self.knodes[knode] = node
        return knode

    def add_nodes_from(self, nodes):
        """ Given an iterable of nodes to add, add them and return an iterable of knodes.
            If a node already exists, its knode is returned in any case. """
        # Dereference: 15% performance gain
        addNode = self.nkG.addNode
        get = self.nodes.get
        setitem_nodes = self.nodes.__setitem__
        setitem_knodes = self.knodes.__setitem__
        #
        for node in nodes:
            knode = get(node, None)
            if knode is None:
                knode = addNode()
                setitem_nodes(node, knode) #nodes[node] = knode
                setitem_knodes(knode, node) #knodes[knode] = node
            yield knode

    def add_edge(self, source, target, weight=1.0):
        """ Adds an edge relating source and target.
            The weight must be a number, or leave it as default (1.0).
            Does not allow duplicated edges (like networkx, and unlike NetworKit).
            If the edge exists, the weight is updated.
            Does not add two edges like networkx: NetworKit has true undirected edges. """
        # Must check that the weight is a number.
        # Will throw a ValueError if it is not a float.
        weight = float(weight)
        ksource = self.add_node(source)
        ktarget = self.add_node(target)
        if self.nkG.hasEdge(ksource, ktarget):
            if self.nkG.isWeighted():
                self.nkG.setWeight(ksource, ktarget, weight)
        else:
            self.nkG.addEdge(ksource, ktarget, weight)

    def add_edges_from(self, edges):
        """ Differs from networkx's add_edges_from in that the tuple
            describing each edge, if it has 3 entries, the 3rd entry
            is the weight, not a dictionary.
            See also: add_edges_from_pairs when individual weights are not needed. """
        edges = iter(edges) # ensure iterator
        # Discover if edges is an iterable of pairs
        edge = next(edges)
        if 2 == len(edge):
            # Choose higher-performance function
            self.add_edge(edge[0], edge[1])
            self.add_edges_from_pairs(edges)
        else:
            self.add_edge(edge[0], edge[1], float(edge[2]))
            is_weighted = self.nkG.isWeighted()
            # Dereference: performance gain
            hasEdge = self.nkG.hasEdge
            addEdge = self.nkG.addEdge
            setWeight = self.nkG.setWeight
            #
            weights = deque() # will only ever have one single value
            def storeWeight(edge):
                weights.append(edge[2])
                return edge[0:2]
            #
            knodes = self.add_nodes_from(chain.from_iterable(map(storeWeight, edges))) # here, map is faster than list comprehension
            for ksource in knodes:
                ktarget = next(knodes)
                w = weights.popleft()
                if hasEdge(ksource, ktarget):
                    if is_weighted:
                        setWeight(ksource, ktarget, float(w))
                else:
                    addEdge(ksource, ktarget, float(w))

        """ # simple but inneficient: far too many unnecessary function calls
        for edge in edges:
            self.add_edge(edge[0], edge[1],
                          weight=float(edge[2]) if len(edge) > 2 else 1.0)
        """

    def add_edges_from_pairs(self, edges, weight=1.0):
        """ Add edges from an iterable of pairs of nodes.
            All edges with default weight of 1.0. """
        weight = float(weight) # ensure number
        is_weighted = self.nkG.isWeighted()
        # Dereference: performance gain
        hasEdge = self.nkG.hasEdge
        addEdge = self.nkG.addEdge
        setWeight = self.nkG.setWeight
        #
        knodes = self.add_nodes_from(chain.from_iterable(edges)) # a generator
        # Consumes two nodes at a time: notice the call to next(knodes)
        for ksource in knodes:
            ktarget = next(knodes)
            if hasEdge(ksource, ktarget):
                if is_weighted:
                    setWeight(ksource, ktarget, weight)
            else:
                addEdge(ksource, ktarget, weight)

    def add_path(self, nodes, weight=1.0):
        weight = float(weight)
        knodes = self.add_nodes_from(nodes)
        knode1 = next(knodes)
        for knode2 in knodes:
            self.nkG.addEdge(knode1, knode2, weight)# faster function call with weight as 3rd arg than as keyword arg with w=weight
            knode1 = knode2

    def add_cycle(self, nodes, weight=1.0):
        weight = float(weight)
        knodes = self.add_nodes_from(nodes)
        knode1 = next(knodes)
        first = knode1
        for knode2 in knodes:
            self.nkG.addEdge(knode1, knode2, weight)
            knode1 = knode2
        self.nkG.addEdge(knode1, first, weight)

    def add_star(self, nodes, weight=1.0):
        """ First node makes an edge to every other node. """
        weight = float(weight)
        knodes = self.add_nodes_from(nodes)
        ksource = next(knodes)
        for ktarget in knodes:
            self.nkG.addEdge(ksource, ktarget, weight)

    def remove_node(self, node):
        knode = self.nodes.get(node, None)
        if knode:
            self.nkG.removeNode(knode)
            del self.nodes[node]
            del self.knodes[knode]

    def remove_nodes_from(self, nodes):
        for node in node:
            self.remove_node(node)

    def remove_edge(self, source, target):
        ksource = self.nodes.get(source, None)
        ktarget = self.nodes.get(target, None)
        if ksource is not None and ktarget is not None:
            self.nkG.removeEdge(ksource, ktarget)

    def remove_edges_from(self, edges):
        for edge in edges:
            self.remove_edge(edge[0], edge[1])
        self.nkG.compactEdges()

    def has_successor(self, node):
        knode = self.nodes.get(node, None)
        if knode is None:
            return False
        return len(self.nkG.neighbors(knode)) > 0

    def has_predecessor(self, node):
        knode = self.nodes.get(node, None)
        if knode is None:
            return False
        if self.nkG.isDirected():
            # Find at least one predecessor: a source that has node as target
            for ksource, ktarget in self.nkG.edges():
                if ktarget == knode:
                    return True
        else:
            return len(self.nkG.neighbors(knode)) > 0

    def number_of_nodes(self):
        return self.nkG.numberOfNodes()

    def size(self):
        """ Number of edges in the graph. """
        return self.nkG.numberOfEdges()

    def number_of_edges(self, source=None, target=None):
        """ Same behavior as networkx.number_of_edges """
        if target is None or source is None:
            return self.nkG.numberOfEdges()
        else:
            if source in self.nodes and target in self.nodes:
                return 1
            else:
                return 0

    def number_of_selfloops(self):
        return self.nkG.numberOfSelfLoops()

    def selfloop_edges(self):
        for ksource, ktarget in self.nkG.edges():
            if ksource == ktarget:
                node = self.knodes[ksource]
                yield (node, node)

    def nodes_with_selfloops(self):
        for node, _ in self.selfloop_edges():
            yield node

    def subgraph(self, nodes):
        sub = self.__class__()
        for node in nodes:
            knode = self.nodes.get(node, None)
            if knode is None:
                continue
            sub.nodes[node] = knode
            sub.knodes[knode] = node
        sub.nkG = self.nkG.subgraphFromNodes(sub.knodes.keys())
        return sub

    def edges(self):
        for ksource, ktarget in self.nkG.edges():
            yield (self.knodes[ksource], self.knodes[ktarget])

    def nodes(self):
        return self.nodes.keys()

    def is_directed(self):
        return self.nkG.isDirected()

    def copy(self, directed=False):
        """ Safely deep-copy this graph. """
        # While it could be made faster, there is no guarantee as to what IDs
        # the NetworKit Graph.addNode function will return.
        copy = Graph(directed=directed)
        for ksource, ktarget in self.nkG.edges():
            copy.add_edge(self.knodes[ksource],
                          self.knodes[ktarget],
                          self.nkG.weight(ksource, ktarget))
        return copy

    def to_undirected(self):
        return self.copy(directed=False)

    def clear(self):
        self.nkG = graph.Graph(weighted=self.nkG.isWeighted(), directed=self.nkG.isDirected())
        self.nodes = {}
        self.knodes = {}

    def __iter__(self):
        """ Return an iterator over all nodes of the graph. """
        return self.nodes.keys()

    def __contains__(self, node):
        """ Return true if node exists in the graph. """
        return node in self.nodes

    def __len__(self):
        """ Return the number of nodes. """
        return len(self.nodes)

    def ___getitem__(self, node):
        """ Return a dictionary of nodes connected to node as keys, and weight as values. """
        knode = self.nodes.get(node, None)
        if knode:
            return {kn: self.nkG.weight(kn) for kn in self.nkG.neighbors(knode)}
        else:
            return {}

    def weight(self, source, target):
        ksource = self.nodes.get(source, None)
        ktarget = self.nodes.get(target, None)
        assert ksource is not None
        assert ktarget is not None
        return self.nkG.weight(ksource, ktarget)

class DiGraph(Graph):
    def __init__(self):
        Graph.__init__(self, directed=True)

    def copy(self, directed=True):
        return super(DiGraph, self).copy(directed=directed)
