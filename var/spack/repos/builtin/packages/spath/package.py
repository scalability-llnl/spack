# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spath(CMakePackage):
    """Represent and manipulate file system paths"""

    homepage = "https://github.com/ecp-veloc/spath"
    url      = "https://github.com/ECP-VeloC/spath/archive/v0.0.2.tar.gz"
    git      = "https://github.com/ecp-veloc/spath.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.0.2', sha256='7a65be59c3d27e92ed4718fba1a97a4a1c68e0a552b54de13d58afe3d8199cf7')
    version('0.0.1', sha256='f41c0ac74e6fb8acfd0c072d756db0fc9c00441f22be492cc4ad25f7fb596a24')

    variant('mpi', default=True, description="Build with MPI support.")
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = []

        if self.spec.satisfies('platform=cray'):
            args.append("-DSPATH_LINK_STATIC=ON")

        if "+mpi" in self.spec:
            args.append('-DMPI=ON')
            args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        else:
            args.append('-DMPI=OFF')

        return args
