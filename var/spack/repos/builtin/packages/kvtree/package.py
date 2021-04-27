# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kvtree(CMakePackage):
    """KVTree provides a fully extensible C datastructure modeled after perl
    hashes."""

    homepage = "https://github.com/ecp-veloc/KVTree"
    url      = "https://github.com/ecp-veloc/KVTree/archive/v1.1.1.tar.gz"
    git      = "https://github.com/ecp-veloc/kvtree.git"

    tags = ['ecp']

    version('master', branch='master')
    version('1.1.1', sha256='4776bd55a559b7f9bb594454ae6b14ebff0087c93c3d59ac7d1ab27df4aa4d74')
    version('1.1.0', sha256='3e6c003e7b8094d7c2d1529a973d68a68f953ffa63dcde5f4c7c7e81ddf06564')
    version('1.0.3', sha256='c742cdb1241ef4cb13767019204d5350a3c4383384bed9fb66680b93ff44b0d4')
    version('1.0.2', sha256='56fb5b747758c24a907a8380e8748d296900d94de9547bc15f6b427ac4ae2ec4')

    variant('mpi', default=True, description="Build with MPI message packing")
    depends_on('mpi', when='+mpi')

    variant('file_lock', default='FLOCK',
            values=('FLOCK', 'FNCTL', 'NONE'),
            multi=False,
            description='File locking style for KVTree.')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.append("-DMPI=ON")
            args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        else:
            args.append("-DMPI=OFF")

        args.append('-DKVTREE_FILE_LOCK={0}'.format(
            self.spec.variants['file_lock'].value.upper()))

        if self.spec.satisfies('platform=cray'):
            args.append("-DKVTREE_LINK_STATIC=ON")
        return args
