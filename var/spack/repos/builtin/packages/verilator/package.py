# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Verilator(AutotoolsPackage):
    """Verilator is the fastest free Verilog HDL simulator.

    It compiles synthesizable Verilog (not test-bench code!), plus some PSL,
    SystemVerilog and Synthesis assertions into C++ or SystemC code. It is
    designed for large projects where fast simulation performance is of primary
    concern, and is especially well suited to generate executable models of
    CPUs for embedded software design teams.

    Please do not download this program if you are expecting a full featured
    replacement for NC-Verilog, VCS or another commercial Verilog simulator
    or Verilog compiler for a little project! (Try Icarus instead.) However, if
    you are looking for a path to migrate synthesizable Verilog to C++ or
    SystemC, and writing just a touch of C code and Makefiles doesn't scare you
    off, this is the free Verilog compiler for you.

    Verilator supports the synthesis subset of Verilog, plus initial
    statements, proper blocking/non-blocking assignments, functions, tasks,
    multi-dimensional arrays, and signed numbers. It also supports very simple
    forms of SystemVerilog assertions and coverage analysis. Verilator supports
    the more important Verilog 2005 constructs, and some SystemVerilog
    features, with additional constructs being added as users request them.

    Verilator has been used to simulate many very large multi-million gate
    designs with thousands of modules."""

    homepage = "https://www.veripool.org/projects/verilator"
    url      = "https://www.veripool.org/ftp/verilator-3.920.tgz"

    version('3.920', sha256='2b5c38aa432d0766a38475219f9548d64d18104ce8bdcb5d29e42f5da06943ff')
    version('3.904', sha256='ea95e08b2d70682ad42e6c2f5ba99f59b2e7b220791214076099cdf6b7a8c1cb')

    depends_on('bison', type='build')
    depends_on('flex')
    depends_on('perl',  type=('build', 'run'))

    def setup_run_environment(self, env):
        env.prepend_path('VERILATOR_ROOT', self.prefix)

    # verilator requires access to its shipped scripts (bin) and include
    # but the standard make doesn't put it in the correct places
    @run_before('install')
    def install_include(self):
        install_tree('include', prefix.include)
        install_tree('bin', prefix.bin)

    # we need to fix the CXX and LINK paths, as they point to the spack
    # wrapper scripts which aren't usable without spack
    @run_after('install')
    def patch_cxx(self):
        filter_file(r'^CXX\s*=.*', 'CXX = {0}'.format(self.compiler.cxx),
                    join_path(self.prefix.include, 'verilated.mk'))
        filter_file(r'^LINK\s*=.*', 'LINK = {0}'.format(self.compiler.cxx),
                    join_path(self.prefix.include, 'verilated.mk'))
