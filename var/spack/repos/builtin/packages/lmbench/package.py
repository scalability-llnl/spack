# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lmbench(MakefilePackage):
    """lmbench is a suite of simple, portable, ANSI/C microbenchmarks for
    UNIX/POSIX. In general, it measures two key features: latency and
    bandwidth. lmbench is intended to give system developers insight into
    basic costs of key operations."""

    homepage = "http://lmbench.sourceforge.net/"
    git      = "https://github.com/intel/lmbench.git"

    version('develop', branch='master')

    patch('lmbench3.patch', sha256='8de24d3c5b90f7b41e3ee1814ea09850bf2cefce929b9cb7e39f269a51fa5d01')

    depends_on('libtirpc')

    def setup_build_environment(self, env):
        env.prepend_path('CPATH', self.spec['libtirpc'].prefix.include.tirpc)

    def build(self, spec, prefix):
        make('build')

    def install(self, spec, prefix):
        install_tree('.', prefix)
