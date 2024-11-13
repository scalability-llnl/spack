# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
r"""Functions for graphing DAGs of dependencies.

This file contains code for graphing DAGs of software packages
(i.e. Spack specs).  There are two main functions you probably care
about:

graph_ascii() will output a colored graph of a spec in ascii format,
kind of like the graph git shows with "git log --graph", e.g.::

    o  mpileaks
    |\
    | |\
    | o |  callpath
    |/| |
    | |\|
    | |\ \
    | | |\ \
    | | | | o  adept-utils
    | |_|_|/|
    |/| | | |
    o | | | |  mpi
     / / / /
    | | o |  dyninst
    | |/| |
    |/|/| |
    | | |/
    | o |  libdwarf
    |/ /
    o |  libelf
     /
    o  boost

graph_dot() will output a graph of a spec (or multiple specs) in dot format.
"""
import enum
import sys
from typing import List, Optional, Set, TextIO, Tuple

import llnl.util.tty.color

import spack.deptypes as dt
import spack.repo
import spack.spec
import spack.tengine
import spack.traverse


def find(seq, predicate):
    """Find index in seq for which predicate is True.

    Searches the sequence and returns the index of the element for
    which the predicate evaluates to True.  Returns -1 if the
    predicate does not evaluate to True for any element in seq.

    """
    for i, elt in enumerate(seq):
        if predicate(elt):
            return i
    return -1


class _GraphLineState(enum.Enum):
    """Names of different graph line states."""

    NODE = enum.auto()
    COLLAPSE = enum.auto()
    MERGE_RIGHT = enum.auto()
    EXPAND_RIGHT = enum.auto()
    BACK_EDGE = enum.auto()


class AsciiGraph:
    def __init__(self):
        # These can be set after initialization or after a call to
        # graph() to change behavior.
        self.node_character = "o"
        self.debug = False
        self.indent = 0
        self.depflag = dt.ALL

        # These are colors in the order they'll be used for edges.
        # See llnl.util.tty.color for details on color characters.
        self.colors = "rgbmcyRGBMCY"

        # Internal vars are used in the graph() function and are initialized there
        self._name_to_color = None  # Node name to color
        self._out = None  # Output stream
        self._frontier = None  # frontier
        self._prev_state = None  # State of previous line
        self._prev_index = None  # Index of expansion point of prev line
        self._pos = None

    def _indent(self):
        self._out.write(self.indent * " ")

    def _write_edge(self, string, index, sub=0):
        """Write a colored edge to the output stream."""
        # Ignore empty frontier entries (they're just collapsed)
        if not self._frontier[index]:
            return
        name = self._frontier[index][sub]
        edge = f"@{self._name_to_color[name]}{{{string}}}"
        self._out.write(edge)

    def _connect_deps(self, i, deps, label=None):
        """Connect dependencies to existing edges in the frontier.

        ``deps`` are to be inserted at position i in the
        frontier. This routine determines whether other open edges
        should be merged with <deps> (if there are other open edges
        pointing to the same place) or whether they should just be
        inserted as a completely new open edge.

        Open edges that are not fully expanded (i.e. those that point
        at multiple places) are left intact.

        Parameters:

        label    -- optional debug label for the connection.

        Returns: True if the deps were connected to another edge
        (i.e. the frontier did not grow) and False if the deps were
        NOT already in the frontier (i.e. they were inserted and the
        frontier grew).

        """
        if len(deps) == 1 and deps in self._frontier:
            j = self._frontier.index(deps)

            # convert a right connection into a left connection
            if i < j:
                self._frontier.pop(j)
                self._frontier.insert(i, deps)
                return self._connect_deps(j, deps, label)

            collapse = True
            if self._prev_state == _GraphLineState.EXPAND_RIGHT:
                # Special case where previous line expanded and i is off by 1.
                self._back_edge_line([], j, i + 1, True, label + "-1.5 " + str((i + 1, j)))
                collapse = False

            else:
                # Previous node also expanded here, so i is off by one.
                if self._prev_state == _GraphLineState.NODE and self._prev_index < i:
                    i += 1

                if i - j > 1:
                    # We need two lines to connect if distance > 1
                    self._back_edge_line([], j, i, True, label + "-1 " + str((i, j)))
                    collapse = False

            self._back_edge_line([j], -1, -1, collapse, label + "-2 " + str((i, j)))
            return True

        if deps:
            self._frontier.insert(i, deps)
            return False

        return False

    def _set_state(self, state, index, label=None):
        self._prev_state = state
        self._prev_index = index

        if self.debug:
            self._out.write(" " * 20)
            self._out.write(f"{str(self._prev_state) if self._prev_state else '':<20}")
            self._out.write(f"{str(label) if label else '':<20}")
            self._out.write(f"{self._frontier}")

    def _back_edge_line(self, prev_ends, end, start, collapse, label=None):
        """Write part of a backwards edge in the graph.

        Writes single- or multi-line backward edges in an ascii graph.
        For example, a single line edge::

            | | | | o |
            | | | |/ /  <-- single-line edge connects two nodes.
            | | | o |

        Or a multi-line edge (requires two calls to back_edge)::

            | | | | o |
            | |_|_|/ /   <-- multi-line edge crosses vertical edges.
            |/| | | |
            o | | | |

        Also handles "pipelined" edges, where the same line contains
        parts of multiple edges::

                      o start
            | |_|_|_|/|
            |/| | |_|/| <-- this line has parts of 2 edges.
            | | |/| | |
            o   o

        Arguments:

        prev_ends -- indices in frontier of previous edges that need
                     to be finished on this line.

        end -- end of the current edge on this line.

        start -- start index of the current edge.

        collapse -- whether the graph will be collapsing (i.e. whether
                    to slant the end of the line or keep it straight)

        label -- optional debug label to print after the line.

        """

        def advance(to_pos, edges):
            """Write edges up to <to_pos>."""
            for i in range(self._pos, to_pos):
                for e in edges():
                    self._write_edge(*e)
                self._pos += 1

        flen = len(self._frontier)
        self._pos = 0
        self._indent()

        for p in prev_ends:
            advance(p, lambda: [("| ", self._pos)])
            advance(p + 1, lambda: [("|/", self._pos)])

        if end >= 0:
            advance(end + 1, lambda: [("| ", self._pos)])
            advance(start - 1, lambda: [("|", self._pos), ("_", end)])
        else:
            advance(start - 1, lambda: [("| ", self._pos)])

        if start >= 0:
            advance(start, lambda: [("|", self._pos), ("/", end)])

        if collapse:
            advance(flen, lambda: [(" /", self._pos)])
        else:
            advance(flen, lambda: [("| ", self._pos)])

        self._set_state(_GraphLineState.BACK_EDGE, end, label)
        self._out.write("\n")

    def _node_label(self, node):
        return node.format("{name}@@{version}{/hash:7}")

    def _node_line(self, index, node):
        """Writes a line with a node at index."""
        self._indent()
        for c in range(index):
            self._write_edge("| ", c)

        self._out.write(f"{self.node_character} ")

        for c in range(index + 1, len(self._frontier)):
            self._write_edge("| ", c)

        self._out.write(self._node_label(node))
        self._set_state(_GraphLineState.NODE, index)
        self._out.write("\n")

    def _collapse_line(self, index):
        """Write a collapsing line after a node was added at index."""
        self._indent()
        for c in range(index):
            self._write_edge("| ", c)
        for c in range(index, len(self._frontier)):
            self._write_edge(" /", c)

        self._set_state(_GraphLineState.COLLAPSE, index)
        self._out.write("\n")

    def _merge_right_line(self, index):
        """Edge at index is same as edge to right.  Merge directly with '\'"""
        self._indent()
        for c in range(index):
            self._write_edge("| ", c)
        self._write_edge("|", index)
        self._write_edge("\\", index + 1)
        for c in range(index + 1, len(self._frontier)):
            self._write_edge("| ", c)

        self._set_state(_GraphLineState.MERGE_RIGHT, index)
        self._out.write("\n")

    def _expand_right_line(self, index):
        self._indent()
        for c in range(index):
            self._write_edge("| ", c)

        self._write_edge("|", index)
        self._write_edge("\\", index + 1)

        for c in range(index + 2, len(self._frontier)):
            self._write_edge(" \\", c)

        self._set_state(_GraphLineState.EXPAND_RIGHT, index)
        self._out.write("\n")

    def write(self, spec, color=None, out=None):
        """Write out an ascii graph of the provided spec.

        Arguments:
        spec -- spec to graph.  This only handles one spec at a time.

        Optional arguments:

        out -- file object to write out to (default is sys.stdout)

        color -- whether to write in color.  Default is to autodetect
                 based on output file.

        """
        if out is None:
            out = sys.stdout

        if color is None:
            color = out.isatty()

        self._out = llnl.util.tty.color.ColorStream(out, color=color)

        # We'll traverse the spec in topological order as we graph it.
        nodes_in_topological_order = [
            edge.spec
            for edge in spack.traverse.traverse_edges_topo(
                [spec], direction="children", deptype=self.depflag
            )
        ]
        nodes_in_topological_order.reverse()

        # Work on a copy to be nondestructive
        spec = spec.copy()

        # Colors associated with each node in the DAG.
        # Edges are colored by the node they point to.
        self._name_to_color = {
            spec.dag_hash(): self.colors[i % len(self.colors)]
            for i, spec in enumerate(nodes_in_topological_order)
        }

        # Frontier tracks open edges of the graph as it's written out.
        self._frontier = [[spec.dag_hash()]]
        while self._frontier:
            # Find an unexpanded part of frontier
            i = find(self._frontier, lambda f: len(f) > 1)

            if i >= 0:
                # Expand frontier until there are enough columns for all children.

                # Figure out how many back connections there are and
                # sort them so we do them in order
                back = []
                for d in self._frontier[i]:
                    b = find(self._frontier[:i], lambda f: f == [d])
                    if b != -1:
                        back.append((b, d))

                # Do all back connections in sorted order so we can
                # pipeline them and save space.
                if back:
                    back.sort()
                    prev_ends = []
                    collapse_l1 = False
                    for j, (b, d) in enumerate(back):
                        self._frontier[i].remove(d)
                        if i - b > 1:
                            collapse_l1 = any(not e for e in self._frontier)
                            self._back_edge_line(prev_ends, b, i, collapse_l1, "left-1")
                            del prev_ends[:]
                        prev_ends.append(b)

                    # Check whether we did ALL the deps as back edges,
                    # in which case we're done.
                    pop = not self._frontier[i]
                    collapse_l2 = pop
                    if collapse_l1:
                        collapse_l2 = False
                    if pop:
                        self._frontier.pop(i)
                    self._back_edge_line(prev_ends, -1, -1, collapse_l2, "left-2")

                elif len(self._frontier[i]) > 1:
                    # Expand forward after doing all back connections

                    if (
                        i + 1 < len(self._frontier)
                        and len(self._frontier[i + 1]) == 1
                        and self._frontier[i + 1][0] in self._frontier[i]
                    ):
                        # We need to connect to the element to the right.
                        # Keep lines straight by connecting directly and
                        # avoiding unnecessary expand/contract.
                        name = self._frontier[i + 1][0]
                        self._frontier[i].remove(name)
                        self._merge_right_line(i)

                    else:
                        # Just allow the expansion here.
                        dep_hash = self._frontier[i].pop(0)
                        deps = [dep_hash]
                        self._frontier.insert(i, deps)
                        self._expand_right_line(i)

                        self._frontier.pop(i)
                        self._connect_deps(i, deps, "post-expand")

                # Handle any remaining back edges to the right
                j = i + 1
                while j < len(self._frontier):
                    deps = self._frontier.pop(j)
                    if not self._connect_deps(j, deps, "back-from-right"):
                        j += 1

            else:
                # Nothing to expand; add dependencies for a node.
                node = nodes_in_topological_order.pop()

                # Find the named node in the frontier and draw it.
                i = find(self._frontier, lambda f: node.dag_hash() in f)
                self._node_line(i, node)

                # Replace node with its dependencies
                self._frontier.pop(i)
                edges = sorted(node.edges_to_dependencies(depflag=self.depflag), reverse=True)
                if edges:
                    deps = [e.spec.dag_hash() for e in edges]
                    self._connect_deps(i, deps, "new-deps")  # anywhere.

                elif self._frontier:
                    self._collapse_line(i)


def graph_ascii(
    spec, node="o", out=None, debug=False, indent=0, color=None, depflag: dt.DepFlag = dt.ALL
):
    graph = AsciiGraph()
    graph.debug = debug
    graph.indent = indent
    graph.node_character = node
    graph.depflag = depflag

    graph.write(spec, color=color, out=out)


class DotGraphBuilder:
    """Visit edges of a graph a build DOT options for nodes and edges"""

    def __init__(self):
        self.nodes: Set[Tuple[str, str]] = set()
        self.edges: Set[Tuple[str, str, str]] = set()

    def visit(self, edge: spack.spec.DependencySpec):
        """Visit an edge and builds up entries to render the graph"""
        if edge.parent is None:
            self.nodes.add(self.node_entry(edge.spec))
            return

        self.nodes.add(self.node_entry(edge.parent))
        self.nodes.add(self.node_entry(edge.spec))
        self.edges.add(self.edge_entry(edge))

    def node_entry(self, node: spack.spec.Spec) -> Tuple[str, str]:
        """Return a tuple of (node_id, node_options)"""
        raise NotImplementedError("Need to be implemented by derived classes")

    def edge_entry(self, edge: spack.spec.DependencySpec) -> Tuple[str, str, str]:
        """Return a tuple of (parent_id, child_id, edge_options)"""
        raise NotImplementedError("Need to be implemented by derived classes")

    def context(self):
        """Return the context to be used to render the DOT graph template"""
        result = {"nodes": self.nodes, "edges": self.edges}
        return result

    def render(self) -> str:
        """Return a string with the output in DOT format"""
        environment = spack.tengine.make_environment()
        template = environment.get_template("misc/graph.dot")
        return template.render(self.context())


class SimpleDAG(DotGraphBuilder):
    """Simple DOT graph, with nodes colored uniformly and edges without properties"""

    def node_entry(self, node):
        format_option = "{name}{@version}{%compiler}{/hash:7}"
        return node.dag_hash(), f'[label="{node.format(format_option)}"]'

    def edge_entry(self, edge):
        return edge.parent.dag_hash(), edge.spec.dag_hash(), None


class StaticDag(DotGraphBuilder):
    """DOT graph for possible dependencies"""

    def node_entry(self, node):
        return node.name, f'[label="{node.name}"]'

    def edge_entry(self, edge):
        return edge.parent.name, edge.spec.name, None


class DAGWithDependencyTypes(DotGraphBuilder):
    """DOT graph with link,run nodes grouped together and edges colored according to
    the dependency types.
    """

    def __init__(self):
        super().__init__()
        self.main_unified_space: Set[str] = set()

    def visit(self, edge):
        if edge.parent is None:
            for node in spack.traverse.traverse_nodes([edge.spec], deptype=dt.LINK | dt.RUN):
                self.main_unified_space.add(node.dag_hash())
        super().visit(edge)

    def node_entry(self, node):
        node_str = node.format("{name}{@version}{%compiler}{/hash:7}")
        options = f'[label="{node_str}", group="build_dependencies", fillcolor="coral"]'
        if node.dag_hash() in self.main_unified_space:
            options = f'[label="{node_str}", group="main_psid"]'
        return node.dag_hash(), options

    def edge_entry(self, edge):
        colormap = {"build": "dodgerblue", "link": "crimson", "run": "goldenrod"}
        label = ""
        if edge.virtuals:
            label = f" xlabel=\"virtuals={','.join(edge.virtuals)}\""
        return (
            edge.parent.dag_hash(),
            edge.spec.dag_hash(),
            f"[color=\"{':'.join(colormap[x] for x in dt.flag_to_tuple(edge.depflag))}\""
            + label
            + "]",
        )


def _static_edges(specs, depflag):
    for spec in specs:
        pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
        possible = pkg_cls.possible_dependencies(expand_virtuals=True, depflag=depflag)

        for parent_name, dependencies in possible.items():
            for dependency_name in dependencies:
                yield spack.spec.DependencySpec(
                    spack.spec.Spec(parent_name),
                    spack.spec.Spec(dependency_name),
                    depflag=depflag,
                    virtuals=(),
                )


def static_graph_dot(
    specs: List[spack.spec.Spec], depflag: dt.DepFlag = dt.ALL, out: Optional[TextIO] = None
):
    """Static DOT graph with edges to all possible dependencies.

    Args:
        specs: abstract specs to be represented
        depflag: dependency types to consider
        out: optional output stream. If None sys.stdout is used
    """
    out = out or sys.stdout
    builder = StaticDag()
    for edge in _static_edges(specs, depflag):
        builder.visit(edge)
    out.write(builder.render())


def graph_dot(
    specs: List[spack.spec.Spec],
    builder: Optional[DotGraphBuilder] = None,
    depflag: dt.DepFlag = dt.ALL,
    out: Optional[TextIO] = None,
):
    """DOT graph of the concrete specs passed as input.

    Args:
        specs: specs to be represented
        builder: builder to use to render the graph
        depflag: dependency types to consider
        out: optional output stream. If None sys.stdout is used
    """
    if not specs:
        raise ValueError("Must provide specs to graph_dot")

    if out is None:
        out = sys.stdout

    builder = builder or SimpleDAG()
    for edge in spack.traverse.traverse_edges(
        specs, cover="edges", order="breadth", deptype=depflag
    ):
        builder.visit(edge)

    out.write(builder.render())
