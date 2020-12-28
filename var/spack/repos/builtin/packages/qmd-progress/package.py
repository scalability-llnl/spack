# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class QmdProgress(CMakePackage):
    """PROGRESS: Parallel, Rapid O(N) and Graph-based Recursive Electronic
    Structure Solver.
    This library is focused on the development of general solvers that are
    commonly used in quantum chemistry packages."""

    homepage = "https://github.com/lanl/qmd-progress"
    url      = "https://github.com/lanl/qmd-progress/tarball/v1.1.0"
    git      = "https://github.com/lanl/qmd-progress.git"

    version('develop', branch='master')
    version('1.1.0', sha256='2c5eac252067bfb55d715c9ce5de2e4306b20b4273979dda15b4a2f71f69bb0b')
    version('1.0.0', sha256='28c99eb80d9a6b09e1d01d61538b3b924850d89c6a8bfb5d3e8b6490be822296')

    variant('graphlib', default=False, description='Build with Metis Suppport')
    variant('mpi', default=True, description='Build with MPI Support')
    variant('shared', default=True, description='Build shared libs')

    depends_on('bml')
    depends_on('mpi', when='+mpi')
    depends_on('metis', when='+graphlib')

    def cmake_args(self):
        spec = self.spec
        args = ['-DCMAKE_Fortran_FLAGS=-ffree-line-length-none']
        if '+shared' in spec:
            args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS=OFF')
        if '+mpi' in spec:
            args.append('-DPROGRESS_MPI=yes')
            args.append('-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc)
            args.append('-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx)
            args.append('-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc)
        else:
            args.append('-DPROGRESS_MPI=no')
        if '+graphlib' in spec:
            args.append('-DPROGRESS_GRAPHLIB=yes')
        else:
            args.append('-DPROGRESS_GRAPHLIB=no')

        return args
