##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from six import StringIO

from spack.spec import Spec
from spack.graph import AsciiGraph, topological_sort, graph_dot


def test_topo_sort(builtin_mock):
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


def test_static_graph_mpileaks(builtin_mock):
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

    assert '  "dyninst" -> "libdwarf"\n'  in dot
    assert '  "callpath" -> "dyninst"\n'  in dot
    assert '  "mpileaks" -> "mpi"\n'      in dot
    assert '  "libdwarf" -> "libelf"\n'   in dot
    assert '  "callpath" -> "mpi"\n'      in dot
    assert '  "mpileaks" -> "callpath"\n' in dot
    assert '  "dyninst" -> "libelf"\n'    in dot


def test_dynamic_dot_graph_mpileaks(builtin_mock):
    """Test dynamically graphing the mpileaks package."""
    s = Spec('mpileaks').normalized()

    stream = StringIO()
    graph_dot([s], static=False, out=stream)

    dot = stream.getvalue()

    mpileaks_hash, mpileaks_lbl = s.dag_hash(), s.format('$_$/')
    mpi_hash, mpi_lbl = s['mpi'].dag_hash(), s['mpi'].format('$_$/')
    callpath_hash, callpath_lbl = (
        s['callpath'].dag_hash(), s['callpath'].format('$_$/'))
    dyninst_hash, dyninst_lbl = (
        s['dyninst'].dag_hash(), s['dyninst'].format('$_$/'))
    libdwarf_hash, libdwarf_lbl = (
        s['libdwarf'].dag_hash(), s['libdwarf'].format('$_$/'))
    libelf_hash, libelf_lbl = (
        s['libelf'].dag_hash(), s['libelf'].format('$_$/'))

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


def test_ascii_graph_mpileaks(builtin_mock):
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
| o  dyninst
| |\
| | o  libdwarf
| |/
| o  libelf
|
o  mpi
'''
