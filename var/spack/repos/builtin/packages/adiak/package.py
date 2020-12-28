# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Adiak(CMakePackage):
    """Adiak collects metadata about HPC application runs and provides it
       to tools."""

    homepage = "https://github.com/LLNL/Adiak"
    url      = "https://github.com/LLNL/Adiak/releases/download/v0.1/adiak-v0.1.1.tar.gz"

    variant('mpi', default=True, description='Build with MPI support')
    variant('shared', default=True, description='Build dynamic libraries')

    version('0.1.1', sha256='438e4652e15e206cd0019423d829fd4f2329323ff0c8861d9586bae051d9624b')

    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.append('-DMPICXX=%s' % self.spec['mpi'].mpicxx)
            args.append('-DMPICC=%s' % self.spec['mpi'].mpicc)
            args.append('-DENABLE_MPI=ON')
        else:
            args.append('-DENABLE_MPI=OFF')

        if (self.spec.satisfies('+shared')):
            args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS=OFF')

        args.append('-DENABLE_TESTS=OFF')
        return args
