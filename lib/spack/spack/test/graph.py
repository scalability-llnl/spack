# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import io

import spack.graph
import spack.spec


def test_dynamic_dot_graph_mpileaks(default_mock_concretization):
    """Test dynamically graphing the mpileaks package."""
    s = default_mock_concretization("mpileaks")
    stream = io.StringIO()
    spack.graph.graph_dot([s], out=stream)
    dot = stream.getvalue()

    nodes_to_check = ["mpileaks", "mpi", "callpath", "dyninst", "libdwarf", "libelf"]
    hashes, builder = {}, spack.graph.SimpleDAG()
    for name in nodes_to_check:
        current = s[name]
        current_hash = current.dag_hash()
        hashes[name] = current_hash
        node_options = builder.node_entry(current)[1]
        assert node_options in dot

    dependencies_to_check = [
        ("dyninst", "libdwarf"),
        ("callpath", "dyninst"),
        ("mpileaks", "mpi"),
        ("libdwarf", "libelf"),
        ("callpath", "mpi"),
        ("mpileaks", "callpath"),
        ("dyninst", "libelf"),
    ]
    for parent, child in dependencies_to_check:
        assert '  "{0}" -> "{1}"\n'.format(hashes[parent], hashes[child]) in dot


def test_ascii_graph_mpileaks(config, mock_packages, monkeypatch):
    monkeypatch.setattr(spack.graph.AsciiGraph, "_node_label", lambda self, node: node.name)
    s = spack.spec.Spec("mpileaks").concretized()

    stream = io.StringIO()
    graph = spack.graph.AsciiGraph()
    graph.write(s, out=stream, color=False)
    graph_str = stream.getvalue()
    graph_str = "\n".join([line.rstrip() for line in graph_str.split("\n")])

    assert (
        graph_str
        == r"""o mpileaks
|\
| o callpath
|/|
o | mpich
 /
o dyninst
|\
| o libdwarf
|/
o libelf
"""
        or graph_str
        == r"""o mpileaks
|\
o | callpath
|\|
| o mpich
|
o dyninst
|\
o | libdwarf
|/
o libelf
"""
    )
