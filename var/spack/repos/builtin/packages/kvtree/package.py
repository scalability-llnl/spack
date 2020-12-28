# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kvtree(CMakePackage):
    """KVTree provides a fully extensible C datastructure modeled after perl
    hashes."""

    homepage = "https://github.com/ecp-veloc/KVTree"
    url      = "https://github.com/ecp-veloc/KVTree/archive/v1.0.2.zip"
    git      = "https://github.com/ecp-veloc/kvtree.git"

    tags = ['ecp']

    version('master', branch='master')
    version('1.0.2', sha256='6b54f4658e5ebab747c0c2472b1505ac1905eefc8a0b2a97d8776f800ee737a3')

    variant('mpi', default=True, description="Build with MPI message packing")
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.append("-DMPI=ON")
            args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        else:
            args.append("-DMPI=OFF")
        if self.spec.satisfies('platform=cray'):
            args.append("-DKVTREE_LINK_STATIC=ON")
        return args
