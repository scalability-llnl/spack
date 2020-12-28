# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Amg2013(MakefilePackage):
    """AMG2013 is a parallel algebraic multigrid solver for linear
    systems arising from problems on unstructured grids.
    It has been derived directly from the BoomerAMG solver in the
    hypre library, a large linear solver library that is being developed
    in the Center for Applied Scientific Computing (CASC) at LLNL.
    """
    tags = ['proxy-app']
    homepage = "https://computing.llnl.gov/projects/co-design/amg2013"
    url      = "https://computing.llnl.gov/projects/co-design/download/amg2013.tgz"

    version('master', sha256='b03771d84a04e3dbbbe32ba5648cd7b789e5853b938dd501e17d23d43f13c50f',
            url='https://computing.llnl.gov/projects/co-design/download/amg2013.tgz')

    variant('openmp', default=True, description='Build with OpenMP support')
    variant('assumedpartition', default=False, description='Use assumed partition (for thousands of processors)')
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

        if '+assumedpartition' in self.spec:
            include_cflags.append('-DHYPRE_NO_GLOBAL_PARTITION')

        if '+int64' in self.spec:
            include_cflags.append('-DHYPRE_LONG_LONG')

        targets.append('INCLUDE_CFLAGS={0}'.format(' '.join(include_cflags)))
        targets.append('INCLUDE_LFLAGS={0}'.format(' '.join(include_lflags)))
        targets.append('CC={0}'.format(self.spec['mpi'].mpicc))

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('test/amg2013', prefix.bin)
        install_tree('docs', prefix.docs)
        install('COPYRIGHT', prefix.docs)
        install('COPYING.LESSER', prefix.docs)
