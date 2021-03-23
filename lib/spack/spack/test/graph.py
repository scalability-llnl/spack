# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from six import StringIO

import spack.repo
from spack.spec import Spec
from spack.graph import AsciiGraph, topological_sort, graph_dot


def test_topo_sort(mock_packages):
    """Test topo sort gives correct order."""
    s = Spec('mpileaks').normalized()

    topo = topological_sort(s)

    assert topo.index('mpileaks') < topo.index('callpath')
    assert topo.index('mpileaks') < topo.index('mpi')
    assert topo.index('mpileaks') < topo.index('dyninst')
    assert topo.index('mpileaks') < topo.index('libdwarf')
    assert topo.index('mpileaks') < topo.index('libelf')

    assert topo.index('callpath') < topo.index('mpi')
    assert topo.index('callpath') < topo.index('dyninst')
    assert topo.index('callpath') < topo.index('libdwarf')
    assert topo.index('callpath') < topo.index('libelf')

    assert topo.index('dyninst') < topo.index('libdwarf')
    assert topo.index('dyninst') < topo.index('libelf')

    assert topo.index('libdwarf') < topo.index('libelf')


def test_static_graph_mpileaks(mock_packages):
    """Test a static spack graph for a simple package."""
    s = Spec('mpileaks').normalized()

    stream = StringIO()
    graph_dot([s], static=True, out=stream)

    dot = stream.getvalue()

    assert '  "mpileaks" [label="mpileaks"]\n' in dot
    assert '  "dyninst" [label="dyninst"]\n'   in dot
    assert '  "callpath" [label="callpath"]\n' in dot
    assert '  "libelf" [label="libelf"]\n'     in dot
    assert '  "libdwarf" [label="libdwarf"]\n' in dot

    mpi_providers = spack.repo.path.providers_for('mpi')
    for spec in mpi_providers:
        assert ('"mpileaks" -> "%s"' % spec.name) in dot
        assert ('"callpath" -> "%s"' % spec.name) in dot

    assert '  "dyninst" -> "libdwarf"\n'  in dot
    assert '  "callpath" -> "dyninst"\n'  in dot
    assert '  "libdwarf" -> "libelf"\n'   in dot
    assert '  "mpileaks" -> "callpath"\n' in dot
    assert '  "dyninst" -> "libelf"\n'    in dot


def test_dynamic_dot_graph_mpileaks(mock_packages, config):
    """Test dynamically graphing the mpileaks package."""
    s = Spec('mpileaks').concretized()

    stream = StringIO()
    graph_dot([s], static=False, out=stream)

    dot = stream.getvalue()
    print(dot)

    mpileaks_hash, mpileaks_lbl = s.dag_hash(), s.format('{name}')
    mpi_hash, mpi_lbl = s['mpi'].dag_hash(), s['mpi'].format('{name}')
    callpath_hash, callpath_lbl = (
        s['callpath'].dag_hash(), s['callpath'].format('{name}'))
    dyninst_hash, dyninst_lbl = (
        s['dyninst'].dag_hash(), s['dyninst'].format('{name}'))
    libdwarf_hash, libdwarf_lbl = (
        s['libdwarf'].dag_hash(), s['libdwarf'].format('{name}'))
    libelf_hash, libelf_lbl = (
        s['libelf'].dag_hash(), s['libelf'].format('{name}'))

    assert '  "%s" [label="%s"]\n' % (mpileaks_hash, mpileaks_lbl) in dot
    assert '  "%s" [label="%s"]\n' % (callpath_hash, callpath_lbl) in dot
    assert '  "%s" [label="%s"]\n' % (mpi_hash,      mpi_lbl) in dot
    assert '  "%s" [label="%s"]\n' % (dyninst_hash,  dyninst_lbl) in dot
    assert '  "%s" [label="%s"]\n' % (libdwarf_hash, libdwarf_lbl) in dot
    assert '  "%s" [label="%s"]\n' % (libelf_hash, libelf_lbl) in dot

    assert '  "%s" -> "%s"\n' % (dyninst_hash, libdwarf_hash)  in dot
    assert '  "%s" -> "%s"\n' % (callpath_hash, dyninst_hash)  in dot
    assert '  "%s" -> "%s"\n' % (mpileaks_hash, mpi_hash)  in dot
    assert '  "%s" -> "%s"\n' % (libdwarf_hash, libelf_hash)  in dot
    assert '  "%s" -> "%s"\n' % (callpath_hash, mpi_hash)  in dot
    assert '  "%s" -> "%s"\n' % (mpileaks_hash, callpath_hash)  in dot
    assert '  "%s" -> "%s"\n' % (dyninst_hash, libelf_hash)  in dot


def test_ascii_graph_mpileaks(mock_packages):
    """Test dynamically graphing the mpileaks package."""
    s = Spec('mpileaks').normalized()

    stream = StringIO()
    graph = AsciiGraph()
    graph.write(s, out=stream, color=False)
    string = stream.getvalue()

    # Some lines in spack graph still have trailing space
    # TODO: fix this.
    string = '\n'.join([line.rstrip() for line in string.split('\n')])

    assert string == r'''o  mpileaks
|\
| o  callpath
|/|
o |  mpi
 /
o  dyninst
|\
| o  libdwarf
|/
o  libelf
'''


def test_topo_sort_filtered(mock_packages):
    """Test topo sort gives correct order when filtering link deps."""
    s = Spec('both-link-and-build-dep-a').normalized()

    topo = topological_sort(s, deptype=('link',))

    assert topo == ['both-link-and-build-dep-a', 'both-link-and-build-dep-c']
