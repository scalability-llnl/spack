# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.deptypes as dt
import spack.traverse as traverse
from spack.spec import Spec


def create_dag(nodes, edges):
    """
    Arguments:
        nodes: list of package names
        edges: list of tuples (from, to, deptype)
    Returns:
        dict: mapping from package name to abstract Spec with proper deps.
    """
    specs = {name: Spec(name) for name in nodes}
    for parent, child, deptypes in edges:
        specs[parent].add_dependency_edge(
            specs[child], depflag=dt.canonicalize(deptypes), virtuals=()
        )
    return specs


@pytest.fixture()
def abstract_specs_dtuse():
    return create_dag(
        nodes=[
            "dtbuild1",
            "dtbuild2",
            "dtbuild3",
            "dtlink1",
            "dtlink2",
            "dtlink3",
            "dtlink4",
            "dtlink5",
            "dtrun1",
            "dtrun2",
            "dtrun3",
            "dttop",
            "dtuse",
        ],
        edges=[
            ("dtbuild1", "dtbuild2", ("build")),
            ("dtbuild1", "dtlink2", ("build", "link")),
            ("dtbuild1", "dtrun2", ("run")),
            ("dtlink1", "dtlink3", ("build", "link")),
            ("dtlink3", "dtbuild2", ("build")),
            ("dtlink3", "dtlink4", ("build", "link")),
            ("dtrun1", "dtlink5", ("build", "link")),
            ("dtrun1", "dtrun3", ("run")),
            ("dtrun3", "dtbuild3", ("build")),
            ("dttop", "dtbuild1", ("build",)),
            ("dttop", "dtlink1", ("build", "link")),
            ("dttop", "dtrun1", ("run")),
            ("dtuse", "dttop", ("build", "link")),
        ],
    )


@pytest.fixture()
def abstract_specs_dt_diamond():
    return create_dag(
        nodes=["dt-diamond", "dt-diamond-left", "dt-diamond-right", "dt-diamond-bottom"],
        edges=[
            ("dt-diamond", "dt-diamond-left", ("build", "link")),
            ("dt-diamond", "dt-diamond-right", ("build", "link")),
            ("dt-diamond-right", "dt-diamond-bottom", ("build", "link", "run")),
            ("dt-diamond-left", "dt-diamond-bottom", ("build")),
        ],
    )


@pytest.fixture()
def abstract_specs_chain():
    # Chain a -> b -> c -> d with skip connections
    # from a -> c and a -> d.
    return create_dag(
        nodes=["chain-a", "chain-b", "chain-c", "chain-d"],
        edges=[
            ("chain-a", "chain-b", ("build", "link")),
            ("chain-b", "chain-c", ("build", "link")),
            ("chain-c", "chain-d", ("build", "link")),
            ("chain-a", "chain-c", ("build", "link")),
            ("chain-a", "chain-d", ("build", "link")),
        ],
    )


@pytest.mark.parametrize("direction", ("children", "parents"))
@pytest.mark.parametrize("deptype", ("all", ("link", "build"), ("run", "link")))
def test_all_orders_traverse_the_same_nodes(direction, deptype, abstract_specs_dtuse):
    # Test whether all graph traversal methods visit the same set of vertices.
    # When testing cover=nodes, the traversal methods may reach the same vertices
    # through different edges, so we're using traverse_nodes here to only verify the
    # vertices.
    #
    # NOTE: root=False currently means "yield nodes discovered at depth > 0",
    # meaning that depth first search will yield dtlink5 as it is first found through
    # dtuse, whereas breadth first search considers dtlink5 at depth 0 and does not
    # yield it since it is a root. Therefore, we only use root=True.
    # (The inconsistency cannot be resolved by making root=False mean "don't yield
    # vertices without in-edges", since this is not how it's used; it's typically used
    # as "skip the input specs".)
    specs = [abstract_specs_dtuse["dtuse"], abstract_specs_dtuse["dtlink5"]]
    kwargs = {"root": True, "direction": direction, "deptype": deptype, "cover": "nodes"}

    def nodes(order):
        s = traverse.traverse_nodes(specs, order=order, **kwargs)
        return sorted(list(s))

    assert nodes("pre") == nodes("post") == nodes("breadth") == nodes("topo")


@pytest.mark.parametrize("direction", ("children", "parents"))
@pytest.mark.parametrize("root", (True, False))
@pytest.mark.parametrize("deptype", ("all", ("link", "build"), ("run", "link")))
def test_all_orders_traverse_the_same_edges(direction, root, deptype, abstract_specs_dtuse):
    # Test whether all graph traversal methods visit the same set of edges.
    # All edges should be returned, including the artificial edges to the input
    # specs when root=True.
    specs = [abstract_specs_dtuse["dtuse"], abstract_specs_dtuse["dtlink5"]]
    kwargs = {"root": root, "direction": direction, "deptype": deptype, "cover": "edges"}

    def edges(order):
        s = traverse.traverse_edges(specs, order=order, **kwargs)
        return sorted(list(s))

    assert edges("pre") == edges("post") == edges("breadth") == edges("topo")


def test_breadth_first_traversal(abstract_specs_dtuse):
    # That that depth of discovery is non-decreasing
    s = abstract_specs_dtuse["dttop"]
    depths = [
        depth
        for (depth, _) in traverse.traverse_nodes(
            [s], order="breadth", key=lambda s: s.name, depth=True
        )
    ]
    assert depths == sorted(depths)


def test_breadth_first_deptype_traversal(abstract_specs_dtuse):
    s = abstract_specs_dtuse["dtuse"]

    names = ["dtuse", "dttop", "dtbuild1", "dtlink1", "dtbuild2", "dtlink2", "dtlink3", "dtlink4"]

    traversal = traverse.traverse_nodes([s], order="breadth", key=id, deptype=("build", "link"))
    assert [x.name for x in traversal] == names


def test_breadth_firsrt_traversal_deptype_with_builddeps(abstract_specs_dtuse):
    s = abstract_specs_dtuse["dttop"]

    names = ["dttop", "dtbuild1", "dtlink1", "dtbuild2", "dtlink2", "dtlink3", "dtlink4"]

    traversal = traverse.traverse_nodes([s], order="breadth", key=id, deptype=("build", "link"))
    assert [x.name for x in traversal] == names


def test_breadth_first_traversal_deptype_full(abstract_specs_dtuse):
    s = abstract_specs_dtuse["dttop"]

    names = [
        "dttop",
        "dtbuild1",
        "dtlink1",
        "dtrun1",
        "dtbuild2",
        "dtlink2",
        "dtrun2",
        "dtlink3",
        "dtlink5",
        "dtrun3",
        "dtlink4",
        "dtbuild3",
    ]

    traversal = traverse.traverse_nodes([s], order="breadth", key=id, deptype="all")
    assert [x.name for x in traversal] == names


def test_breadth_first_traversal_deptype_run(abstract_specs_dtuse):
    s = abstract_specs_dtuse["dttop"]
    names = ["dttop", "dtrun1", "dtrun3"]
    traversal = traverse.traverse_nodes([s], order="breadth", key=id, deptype="run")
    assert [x.name for x in traversal] == names


def test_breadth_first_traversal_reverse(abstract_specs_dt_diamond):
    gen = traverse.traverse_nodes(
        [abstract_specs_dt_diamond["dt-diamond-bottom"]],
        order="breadth",
        key=id,
        direction="parents",
        depth=True,
    )
    assert [(depth, spec.name) for (depth, spec) in gen] == [
        (0, "dt-diamond-bottom"),
        (1, "dt-diamond-left"),
        (1, "dt-diamond-right"),
        (2, "dt-diamond"),
    ]


def test_breadth_first_traversal_multiple_input_specs(abstract_specs_dt_diamond):
    # With DFS, the branch dt-diamond -> dt-diamond-left -> dt-diamond-bottom
    # is followed, with BFS, dt-diamond-bottom should be traced through the second
    # input spec dt-diamond-right at depth 1 instead.
    input_specs = [
        abstract_specs_dt_diamond["dt-diamond"],
        abstract_specs_dt_diamond["dt-diamond-right"],
    ]
    gen = traverse.traverse_edges(input_specs, order="breadth", key=id, depth=True, root=False)
    assert [(depth, edge.parent.name, edge.spec.name) for (depth, edge) in gen] == [
        (1, "dt-diamond", "dt-diamond-left"),  # edge from first input spec "to" depth 1
        (1, "dt-diamond-right", "dt-diamond-bottom"),  # edge from second input spec "to" depth 1
    ]


def test_breadth_first_versus_depth_first_tree(abstract_specs_chain):
    """
    The packages chain-a, chain-b, chain-c, chain-d have the following DAG:
    a --> b --> c --> d # a chain
    a --> c # and "skip" connections
    a --> d
    Here we test at what depth the nodes are discovered when using BFS vs DFS.
    """
    s = abstract_specs_chain["chain-a"]

    # BFS should find all nodes as direct deps
    assert [
        (depth, edge.spec.name)
        for (depth, edge) in traverse.traverse_tree([s], cover="nodes", depth_first=False)
    ] == [(0, "chain-a"), (1, "chain-b"), (1, "chain-c"), (1, "chain-d")]

    # DFS will disover all nodes along the chain a -> b -> c -> d.
    assert [
        (depth, edge.spec.name)
        for (depth, edge) in traverse.traverse_tree([s], cover="nodes", depth_first=True)
    ] == [(0, "chain-a"), (1, "chain-b"), (2, "chain-c"), (3, "chain-d")]

    # When covering all edges, we should never exceed depth 2 in BFS.
    assert [
        (depth, edge.spec.name)
        for (depth, edge) in traverse.traverse_tree([s], cover="edges", depth_first=False)
    ] == [
        (0, "chain-a"),
        (1, "chain-b"),
        (2, "chain-c"),
        (1, "chain-c"),
        (2, "chain-d"),
        (1, "chain-d"),
    ]

    # In DFS we see the chain again.
    assert [
        (depth, edge.spec.name)
        for (depth, edge) in traverse.traverse_tree([s], cover="edges", depth_first=True)
    ] == [
        (0, "chain-a"),
        (1, "chain-b"),
        (2, "chain-c"),
        (3, "chain-d"),
        (1, "chain-c"),
        (1, "chain-d"),
    ]


@pytest.mark.parametrize("cover", ["nodes", "edges"])
@pytest.mark.parametrize("depth_first", [True, False])
def test_tree_traversal_with_key(cover, depth_first, abstract_specs_chain):
    """Compare two multisource traversals of the same DAG. In one case the DAG consists of unique
    Spec instances, in the second case there are identical copies of nodes and edges. Traversal
    should be equivalent when nodes are identified by dag_hash."""
    a = abstract_specs_chain["chain-a"]
    c = abstract_specs_chain["chain-c"]
    kwargs = {"cover": cover, "depth_first": depth_first}
    dag_hash = lambda s: s.dag_hash()

    # Traverse DAG spanned by a unique set of Spec instances
    first = traverse.traverse_tree([a, c], key=id, **kwargs)

    # Traverse equivalent DAG with copies of Spec instances included, keyed by dag hash.
    second = traverse.traverse_tree([a, c.copy()], key=dag_hash, **kwargs)

    # Check that the same nodes are discovered at the same depth
    node_at_depth_first = [(depth, dag_hash(edge.spec)) for (depth, edge) in first]
    node_at_depth_second = [(depth, dag_hash(edge.spec)) for (depth, edge) in second]
    assert node_at_depth_first == node_at_depth_second


def test_breadth_first_versus_depth_first_printing(abstract_specs_chain):
    """Test breadth-first versus depth-first tree printing."""
    s = abstract_specs_chain["chain-a"]

    args = {"format": "{name}", "color": False}

    dfs_tree_nodes = """\
chain-a
    ^chain-b
        ^chain-c
            ^chain-d
"""
    assert s.tree(depth_first=True, **args) == dfs_tree_nodes

    bfs_tree_nodes = """\
chain-a
    ^chain-b
    ^chain-c
    ^chain-d
"""
    assert s.tree(depth_first=False, **args) == bfs_tree_nodes

    dfs_tree_edges = """\
chain-a
    ^chain-b
        ^chain-c
            ^chain-d
    ^chain-c
    ^chain-d
"""
    assert s.tree(depth_first=True, cover="edges", **args) == dfs_tree_edges

    bfs_tree_edges = """\
chain-a
    ^chain-b
        ^chain-c
    ^chain-c
        ^chain-d
    ^chain-d
"""
    assert s.tree(depth_first=False, cover="edges", **args) == bfs_tree_edges


@pytest.fixture()
def abstract_specs_toposort():
    # Create a graph that both BFS and DFS would not traverse in topo order, given the
    # default edge ordering (by target spec name). Roots are {A, E} in forward order
    # and {F, G} in backward order.
    # forward: DFS([A, E]) traverses [A, B, F, G, C, D, E] (not topo since C < B)
    # forward: BFS([A, E]) traverses [A, E, B, C, D, F, G] (not topo since C < B)
    # reverse: DFS([F, G]) traverses [F, B, A, D, C, E, G] (not topo since D < A)
    # reverse: BFS([F, G]) traverses [F, G, B, A, D, C, E] (not topo since D < A)
    # E
    # | A
    # | | \
    # | C |
    # \ | |
    #   D |
    #   | /
    #   B
    #  / \
    # F   G
    return create_dag(
        nodes=["A", "B", "C", "D", "E", "F", "G"],
        edges=(
            ("A", "B", "all"),
            ("A", "C", "all"),
            ("B", "F", "all"),
            ("B", "G", "all"),
            ("C", "D", "all"),
            ("D", "B", "all"),
            ("E", "D", "all"),
        ),
    )


def test_traverse_nodes_topo(abstract_specs_toposort):
    # Test whether we get topologically ordered specs when using traverse_nodes with
    # order=topo and cover=nodes.
    nodes = abstract_specs_toposort

    def test_topo(input_specs, direction="children"):
        # Ensure the invariant that all parents of specs[i] are in specs[0:i]
        specs = list(
            traverse.traverse_nodes(input_specs, order="topo", cover="nodes", direction=direction)
        )
        reverse = "parents" if direction == "children" else "children"
        for i in range(len(specs)):
            parents = specs[i].traverse(cover="nodes", direction=reverse, root=False)
            assert set(list(parents)).issubset(set(specs[:i]))

    # Traverse forward from roots A and E and a non-root D. Notice that adding D has no
    # effect, it's just to make the test case a bit more complicated, as D is a starting
    # point for traversal, but it's also discovered as a descendant of E and A.
    test_topo([nodes["D"], nodes["E"], nodes["A"]], direction="children")

    # Traverse reverse from leafs F and G and non-leaf D
    test_topo([nodes["F"], nodes["D"], nodes["G"]], direction="parents")


def test_traverse_edges_topo(abstract_specs_toposort):
    # Test the invariant that for each node in-edges precede out-edges when
    # using traverse_edges with order=topo.
    nodes = abstract_specs_toposort
    input_specs = [nodes["E"], nodes["A"]]

    # Collect pairs of (parent spec name, child spec name)
    edges = [
        (e.parent.name, e.spec.name)
        for e in traverse.traverse_edges(input_specs, order="topo", cover="edges", root=False)
    ]

    # See figure above, we have 7 edges (excluding artifical ones to the root)
    assert set(edges) == set(
        [("A", "B"), ("A", "C"), ("B", "F"), ("B", "G"), ("C", "D"), ("D", "B"), ("E", "D")]
    )

    # Verify that all in-edges precede all out-edges
    for node in nodes.keys():
        in_edge_indices = [i for (i, (parent, child)) in enumerate(edges) if node == child]
        out_edge_indices = [i for (i, (parent, child)) in enumerate(edges) if node == parent]
        if in_edge_indices and out_edge_indices:
            assert max(in_edge_indices) < min(out_edge_indices)


def test_traverse_nodes_no_deps(abstract_specs_dtuse):
    """Traversing nodes without deps should be the same as deduplicating the input specs. This may
    not look useful, but can be used to avoid a branch on the call site in which it's otherwise
    easy to forget to deduplicate input specs."""
    inputs = [
        abstract_specs_dtuse["dtuse"],
        abstract_specs_dtuse["dtlink5"],
        abstract_specs_dtuse["dtuse"],  # <- duplicate
    ]
    outputs = [x for x in traverse.traverse_nodes(inputs, deptype=dt.NONE)]
    assert outputs == [abstract_specs_dtuse["dtuse"], abstract_specs_dtuse["dtlink5"]]
