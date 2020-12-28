# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Amg(MakefilePackage):
    """AMG is a parallel algebraic multigrid solver for linear systems arising
       from problems on unstructured grids.  The driver provided with AMG
       builds linear systems for various 3-dimensional problems.
    """
    tags = ['proxy-app', 'ecp-proxy-app']

    homepage = "https://computing.llnl.gov/projects/co-design/amg2013"
    git      = "https://github.com/LLNL/AMG.git"

    version('develop', branch='master')
    version('1.2', tag='1.2')
    version('1.1', tag='1.1')
    version('1.0', tag='1.0')

    variant('openmp', default=True, description='Build with OpenMP support')
    variant('optflags', default=False, description='Additional optimizations')
    variant('int64', default=False, description='Use 64-bit integers for global variables')

    depends_on('mpi')

    @property
    def build_targets(self):
        targets = []

        include_cflags = ['-DTIMER_USE_MPI']
        include_lflags = ['-lm']

        if '+openmp' in self.spec:
            include_cflags.append('-DHYPRE_USING_OPENMP')
            include_cflags.append(self.compiler.openmp_flag)
            include_lflags.append(self.compiler.openmp_flag)
            if '+optflags' in self.spec:
                include_cflags.append('-DHYPRE_USING_PERSISTENT_COMM')
                include_cflags.append('-DHYPRE_HOPSCOTCH')

        if '+int64' in self.spec:
            include_cflags.append('-DHYPRE_BIGINT')

        targets.append('INCLUDE_CFLAGS={0}'.format(' '.join(include_cflags)))
        targets.append('INCLUDE_LFLAGS={0}'.format(' '.join(include_lflags)))
        targets.append('CC={0}'.format(self.spec['mpi'].mpicc))

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('test/amg', prefix.bin)
        install_tree('docs', prefix.docs)
