# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from collections import defaultdict
from typing import NamedTuple, Union

import spack.deptypes as dt
import spack.spec

# Export only the high-level API.
__all__ = ["traverse_edges", "traverse_nodes", "traverse_tree"]


#: Data class that stores a directed edge together with depth at
#: which the target vertex was found. It is passed to ``accept``
#: and ``neighbors`` of visitors, so they can decide whether to
#: follow the edge or not.
class EdgeAndDepth(NamedTuple):
    edge: "spack.spec.DependencySpec"
    depth: int


def sort_edges(edges):
    edges.sort(key=lambda edge: (edge.spec.name or "", edge.spec.abstract_hash or ""))
    return edges


class BaseVisitor:
    """A simple visitor that accepts all edges unconditionally and follows all
    edges to dependencies of a given ``deptype``."""

    def __init__(self, depflag: dt.DepFlag = dt.ALL):
        self.depflag = depflag

    def accept(self, item):
        """
        Arguments:
            item (EdgeAndDepth): Provides the depth and the edge through which the
                node was discovered

        Returns:
            bool: Returns ``True`` if the node is accepted. When ``False``, this
                indicates that the node won't be yielded by iterators and dependencies
                are not followed.
        """
        return True

    def neighbors(self, item):
        return sort_edges(item.edge.spec.edges_to_dependencies(depflag=self.depflag))


class ReverseVisitor:
    """A visitor that reverses the arrows in the DAG, following dependents."""

    def __init__(self, visitor, depflag: dt.DepFlag = dt.ALL):
        self.visitor = visitor
        self.depflag = depflag

    def accept(self, item):
        return self.visitor.accept(item)

    def neighbors(self, item):
        """Return dependents, note that we actually flip the edge direction to allow
        generic programming"""
        spec = item.edge.spec
        return sort_edges(
            [edge.flip() for edge in spec.edges_from_dependents(depflag=self.depflag)]
        )


class CoverNodesVisitor:
    """A visitor that traverses each node once."""

    def __init__(self, visitor, key=id, visited=None):
        self.visitor = visitor
        self.key = key
        self.visited = set() if visited is None else visited

    def accept(self, item):
        # Covering nodes means: visit nodes once and only once.
        key = self.key(item.edge.spec)

        if key in self.visited:
            return False

        accept = self.visitor.accept(item)
        self.visited.add(key)
        return accept

    def neighbors(self, item):
        return self.visitor.neighbors(item)


class CoverEdgesVisitor:
    """A visitor that traverses all edges once."""

    def __init__(self, visitor, key=id, visited=None):
        self.visitor = visitor
        self.visited = set() if visited is None else visited
        self.key = key

    def accept(self, item):
        return self.visitor.accept(item)

    def neighbors(self, item):
        # Covering edges means: drop dependencies of visited nodes.
        key = self.key(item.edge.spec)

        if key in self.visited:
            return []

        self.visited.add(key)
        return self.visitor.neighbors(item)


class TopoVisitor:
    """Visitor that can be used in :py:func:`depth-first traversal
    <spack.traverse.traverse_depth_first_with_visitor>` to generate
    a topologically ordered list of specs.

    Algorithm based on "Section 22.4: Topological sort", Introduction to Algorithms
    (2001, 2nd edition) by Cormen, Thomas H.; Leiserson, Charles E.; Rivest, Ronald L.;
    Stein, Clifford.

    Summary of the algorithm: prepend each vertex to a list in depth-first post-order,
    not following edges to nodes already seen. This ensures all descendants occur after
    their parent, yielding a topological order.

    Note: in this particular implementation we collect the *edges* through which the
    vertices are discovered, meaning that a topological order of *vertices* is obtained
    by taking the specs pointed to: ``map(lambda edge: edge.spec, visitor.edges)``.
    Lastly, ``all_edges=True`` can be used to retrieve a list of all reachable
    edges, with the property that for each vertex all in-edges precede all out-edges.
    """

    def __init__(self, visitor, key=id, root=True, all_edges=False):
        """
        Arguments:
            visitor: visitor that implements accept(), pre(), post() and neighbors()
            key: uniqueness key for nodes
            root (bool): Whether to include the root node.
            all_edges (bool): when ``False`` (default): Each node is reached once,
                and ``map(lambda edge: edge.spec, visitor.edges)`` is topologically
                ordered. When ``True``, every edge is listed, ordered such that for
                each node all in-edges precede all out-edges.
        """
        self.visited = set()
        self.visitor = visitor
        self.key = key
        self.root = root
        self.reverse_order = []
        self.all_edges = all_edges

    def accept(self, item):
        if self.key(item.edge.spec) not in self.visited:
            return True
        if self.all_edges and (self.root or item.depth > 0):
            self.reverse_order.append(item.edge)
        return False

    def pre(self, item):
        # You could add a temporary marker for cycle detection
        # that's cleared in `post`, but we assume no cycles.
        pass

    def post(self, item):
        self.visited.add(self.key(item.edge.spec))
        if self.root or item.depth > 0:
            self.reverse_order.append(item.edge)

    def neighbors(self, item):
        return self.visitor.neighbors(item)

    @property
    def edges(self):
        """Return edges in topological order (in-edges precede out-edges)."""
        return list(reversed(self.reverse_order))


def get_visitor_from_args(
    cover, direction, depflag: Union[dt.DepFlag, dt.DepTypes], key=id, visited=None, visitor=None
):
    """
    Create a visitor object from common keyword arguments.

    Arguments:
        cover (str): Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        direction (str): ``children`` or ``parents``. If ``children``, does a traversal
            of this spec's children.  If ``parents``, traverses upwards in the DAG
            towards the root.
        deptype: allowed dependency types
        key: function that takes a spec and outputs a key for uniqueness test.
        visited (set or None): a set of nodes not to follow (when using cover=nodes/edges)
        visitor: An initial visitor that is used for composition.

    Returns:
        A visitor
    """
    if not isinstance(depflag, dt.DepFlag):
        depflag = dt.canonicalize(depflag)
    visitor = visitor or BaseVisitor(depflag)
    if cover == "nodes":
        visitor = CoverNodesVisitor(visitor, key, visited)
    elif cover == "edges":
        visitor = CoverEdgesVisitor(visitor, key, visited)
    if direction == "parents":
        visitor = ReverseVisitor(visitor, depflag)
    return visitor


def with_artificial_edges(specs):
    """Initialize a list of edges from an imaginary root node to the root specs."""
    return [
        EdgeAndDepth(
            edge=spack.spec.DependencySpec(parent=None, spec=s, depflag=0, virtuals=()), depth=0
        )
        for s in specs
    ]


def traverse_depth_first_edges_generator(edges, visitor, post_order=False, root=True, depth=False):
    """Generator that takes explores a DAG in depth-first fashion starting from
    a list of edges. Note that typically DFS would take a vertex not a list of edges,
    but the API is like this so we don't have to create an artificial root node when
    traversing from multiple roots in a DAG.

    Arguments:
        edges (list): List of EdgeAndDepth instances
        visitor: class instance implementing accept() and neigbors()
        post_order (bool): Whether to yield nodes when backtracking
        root (bool): whether to yield at depth 0
        depth (bool): when ``True`` yield a tuple of depth and edge, otherwise only the
            edge.
    """
    for edge in edges:
        if not visitor.accept(edge):
            continue

        yield_me = root or edge.depth > 0

        # Pre
        if yield_me and not post_order:
            yield (edge.depth, edge.edge) if depth else edge.edge

        neighbors = [EdgeAndDepth(edge=n, depth=edge.depth + 1) for n in visitor.neighbors(edge)]

        # This extra branch is just for efficiency.
        if len(neighbors) > 0:
            for item in traverse_depth_first_edges_generator(
                neighbors, visitor, post_order, root, depth
            ):
                yield item

        # Post
        if yield_me and post_order:
            yield (edge.depth, edge.edge) if depth else edge.edge


def traverse_breadth_first_edges_generator(queue, visitor, root=True, depth=False):
    while len(queue) > 0:
        edge = queue.pop(0)

        # If the visitor doesn't accept the node, we don't yield it nor follow its edges.
        if not visitor.accept(edge):
            continue

        if root or edge.depth > 0:
            yield (edge.depth, edge.edge) if depth else edge.edge

        for e in visitor.neighbors(edge):
            queue.append(EdgeAndDepth(e, edge.depth + 1))


def traverse_breadth_first_with_visitor(specs, visitor):
    """Performs breadth first traversal for a list of specs (not a generator).

    Arguments:
        specs (list): List of Spec instances.
        visitor: object that implements accept and neighbors interface, see
            for example BaseVisitor.
    """
    queue = with_artificial_edges(specs)
    while len(queue) > 0:
        edge = queue.pop(0)

        # If the visitor doesn't accept the node, we don't traverse it further.
        if not visitor.accept(edge):
            continue

        for e in visitor.neighbors(edge):
            queue.append(EdgeAndDepth(e, edge.depth + 1))


def traverse_depth_first_with_visitor(edges, visitor):
    """Traverse a DAG in depth-first fashion using a visitor, starting from
    a list of edges. Note that typically DFS would take a vertex not a list of edges,
    but the API is like this so we don't have to create an artificial root node when
    traversing from multiple roots in a DAG.

    Arguments:
        edges (list): List of EdgeAndDepth instances
        visitor: class instance implementing accept(), pre(), post() and neighbors()
    """
    for edge in edges:
        if not visitor.accept(edge):
            continue

        visitor.pre(edge)

        neighbors = [EdgeAndDepth(edge=e, depth=edge.depth + 1) for e in visitor.neighbors(edge)]

        traverse_depth_first_with_visitor(neighbors, visitor)

        visitor.post(edge)


# Helper functions for generating a tree using breadth-first traversal


def breadth_first_to_tree_edges(roots, deptype="all", key=id):
    """This produces an adjacency list (with edges) and a map of parents.
    There may be nodes that are reached through multiple edges. To print as
    a tree, one should use the parents dict to verify if the path leading to
    the node is through the correct parent. If not, the branch should be
    truncated."""
    edges = defaultdict(list)
    parents = dict()

    for edge in traverse_edges(roots, order="breadth", cover="edges", deptype=deptype, key=key):
        parent_id = None if edge.parent is None else key(edge.parent)
        child_id = key(edge.spec)
        edges[parent_id].append(edge)
        if child_id not in parents:
            parents[child_id] = parent_id

    return edges, parents


def breadth_first_to_tree_nodes(roots, deptype="all", key=id):
    """This produces a list of edges that forms a tree; every node has no more
    that one incoming edge."""
    edges = defaultdict(list)

    for edge in traverse_edges(roots, order="breadth", cover="nodes", deptype=deptype, key=key):
        parent_id = None if edge.parent is None else key(edge.parent)
        edges[parent_id].append(edge)

    return edges


def traverse_breadth_first_tree_edges(parent_id, edges, parents, key=id, depth=0):
    """Do a depth-first search on edges generated by bread-first traversal,
    which can be used to produce a tree."""
    for edge in edges[parent_id]:
        yield (depth, edge)

        child_id = key(edge.spec)

        # Don't follow further if we're not the parent
        if parents[child_id] != parent_id:
            continue

        # yield from ... in Python 3.
        for item in traverse_breadth_first_tree_edges(child_id, edges, parents, key, depth + 1):
            yield item


def traverse_breadth_first_tree_nodes(parent_id, edges, key=id, depth=0):
    for edge in edges[parent_id]:
        yield (depth, edge)
        for item in traverse_breadth_first_tree_nodes(key(edge.spec), edges, key, depth + 1):
            yield item


# Topologic order
def traverse_edges_topo(
    specs,
    direction="children",
    deptype: Union[dt.DepFlag, dt.DepTypes] = "all",
    key=id,
    root=True,
    all_edges=False,
):
    """
    Returns a list of edges in topological order, in the sense that all in-edges of a
    vertex appear before all out-edges. By default with direction=children edges are
    directed from dependent to dependency. With directions=parents, the edges are
    directed from dependency to dependent.

    Arguments:
        specs (list): List of root specs (considered to be depth 0)
        direction (str): ``children`` (edges are directed from dependent to dependency)
            or ``parents`` (edges are flipped / directed from dependency to dependent)
        deptype: allowed dependency types
        key: function that takes a spec and outputs a key for uniqueness test.
        root (bool): Yield the root nodes themselves
        all_edges (bool): When ``False`` only one in-edge per node is returned, when
            ``True`` all reachable edges are returned.
    """
    if not isinstance(deptype, dt.DepFlag):
        deptype = dt.canonicalize(deptype)
    visitor: Union[BaseVisitor, ReverseVisitor, TopoVisitor] = BaseVisitor(deptype)
    if direction == "parents":
        visitor = ReverseVisitor(visitor, deptype)
    visitor = TopoVisitor(visitor, key=key, root=root, all_edges=all_edges)
    traverse_depth_first_with_visitor(with_artificial_edges(specs), visitor)
    return visitor.edges


# High-level API: traverse_edges, traverse_nodes, traverse_tree.


def traverse_edges(
    specs,
    root=True,
    order="pre",
    cover="nodes",
    direction="children",
    deptype: Union[dt.DepFlag, dt.DepTypes] = "all",
    depth=False,
    key=id,
    visited=None,
):
    """
    Generator that yields edges from the DAG, starting from a list of root specs.

    Arguments:

        specs (list): List of root specs (considered to be depth 0)
        root (bool): Yield the root nodes themselves
        order (str): What order of traversal to use in the DAG. For depth-first
            search this can be ``pre`` or ``post``. For BFS this should be ``breadth``.
            For topological order use ``topo``
        cover (str): Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        direction (str): ``children`` or ``parents``. If ``children``, does a traversal
            of this spec's children.  If ``parents``, traverses upwards in the DAG
            towards the root.
        deptype: allowed dependency types
        depth (bool): When ``False``, yield just edges. When ``True`` yield
            the tuple (depth, edge), where depth corresponds to the depth
            at which edge.spec was discovered.
        key: function that takes a spec and outputs a key for uniqueness test.
        visited (set or None): a set of nodes not to follow

    Returns:
        A generator that yields ``DependencySpec`` if depth is ``False``
        or a tuple of ``(depth, DependencySpec)`` if depth is ``True``.
    """

    if order == "topo":
        if cover == "paths":
            raise ValueError("cover=paths not supported for order=topo")
        # TODO: There is no known need for topological ordering of traversals (edge or node)
        # with an initialized "visited" set. Revisit if needed.
        if visited is not None:
            raise ValueError("visited set not implemented for order=topo")
        return traverse_edges_topo(
            specs, direction, deptype, key, root, all_edges=cover == "edges"
        )

    root_edges = with_artificial_edges(specs)
    visitor = get_visitor_from_args(cover, direction, deptype, key, visited)

    # Depth-first
    if order in ("pre", "post"):
        return traverse_depth_first_edges_generator(
            root_edges, visitor, order == "post", root, depth
        )
    elif order == "breadth":
        return traverse_breadth_first_edges_generator(root_edges, visitor, root, depth)

    raise ValueError("Unknown order {}".format(order))


def traverse_nodes(
    specs,
    root=True,
    order="pre",
    cover="nodes",
    direction="children",
    deptype: Union[dt.DepFlag, dt.DepTypes] = "all",
    depth=False,
    key=id,
    visited=None,
):
    """
    Generator that yields specs from the DAG, starting from a list of root specs.

    Arguments:
        specs (list): List of root specs (considered to be depth 0)
        root (bool): Yield the root nodes themselves
        order (str): What order of traversal to use in the DAG. For depth-first
            search this can be ``pre`` or ``post``. For BFS this should be ``breadth``.
        cover (str): Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        direction (str): ``children`` or ``parents``. If ``children``, does a traversal
            of this spec's children.  If ``parents``, traverses upwards in the DAG
            towards the root.
        deptype: allowed dependency types
        depth (bool): When ``False``, yield just edges. When ``True`` yield
            the tuple ``(depth, edge)``, where depth corresponds to the depth
            at which ``edge.spec`` was discovered.
        key: function that takes a spec and outputs a key for uniqueness test.
        visited (set or None): a set of nodes not to follow

    Yields:
        By default :class:`~spack.spec.Spec`, or a tuple ``(depth, Spec)`` if depth is
        set to ``True``.
    """
    for item in traverse_edges(specs, root, order, cover, direction, deptype, depth, key, visited):
        yield (item[0], item[1].spec) if depth else item.spec


def traverse_tree(
    specs, cover="nodes", deptype: Union[dt.DepFlag, dt.DepTypes] = "all", key=id, depth_first=True
):
    """
    Generator that yields ``(depth, DependencySpec)`` tuples in the depth-first
    pre-order, so that a tree can be printed from it.

    Arguments:

        specs (list): List of root specs (considered to be depth 0)
        cover (str): Determines how extensively to cover the dag.  Possible values:
            ``nodes`` -- Visit each unique node in the dag only once.
            ``edges`` -- If a node has been visited once but is reached along a
            new path, it's accepted, but not recurisvely followed. This traverses
            each 'edge' in the DAG once.
            ``paths`` -- Explore every unique path reachable from the root.
            This descends into visited subtrees and will accept nodes multiple
            times if they're reachable by multiple paths.
        deptype: allowed dependency types
        key: function that takes a spec and outputs a key for uniqueness test.
        depth_first (bool): Explore the tree in depth-first or breadth-first order.
            When setting ``depth_first=True`` and ``cover=nodes``, each spec only
            occurs once at the shallowest level, which is useful when rendering
            the tree in a terminal.

    Returns:
        A generator that yields ``(depth, DependencySpec)`` tuples in such an order
        that a tree can be printed.
    """
    # BFS only makes sense when going over edges and nodes, for paths the tree is
    # identical to DFS, which is much more efficient then.
    if not depth_first and cover == "edges":
        edges, parents = breadth_first_to_tree_edges(specs, deptype, key)
        return traverse_breadth_first_tree_edges(None, edges, parents, key)
    elif not depth_first and cover == "nodes":
        edges = breadth_first_to_tree_nodes(specs, deptype, key)
        return traverse_breadth_first_tree_nodes(None, edges, key)

    return traverse_edges(specs, order="pre", cover=cover, deptype=deptype, key=key, depth=True)


def by_dag_hash(s: "spack.spec.Spec") -> str:
    """Used very often as a key function for traversals."""
    return s.dag_hash()
