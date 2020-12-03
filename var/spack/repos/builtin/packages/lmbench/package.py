# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

from spack.util.provides import setup_libtirpc_build_environment


class Lmbench(MakefilePackage):
    """lmbench is a suite of simple, portable, ANSI/C microbenchmarks for
    UNIX/POSIX. In general, it measures two key features: latency and
    bandwidth. lmbench is intended to give system developers insight into
    basic costs of key operations."""

    homepage = "http://lmbench.sourceforge.net/"
    git      = "https://github.com/intel/lmbench.git"

    version('master', branch='master')

    depends_on('libtirpc')

    patch('fix_results_path_for_aarch64.patch', sha256='2af57abc9058c56b6dd0697bb01a98902230bef92b117017e318faba148eef60', when='target=aarch64:')

    def setup_build_environment(self, env):
        setup_libtirpc_build_environment(self.spec, env)

    def build(self, spec, prefix):
        make('build')

    def install(self, spec, prefix):
        install_tree('.', prefix)
