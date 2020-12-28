# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shuffile(CMakePackage):
    """Shuffle files between MPI ranks"""

    homepage = "https://github.com/ecp-veloc/shuffile"
    url      = "https://github.com/ecp-veloc/shuffile/archive/v0.0.3.zip"
    git      = "https://github.com/ecp-veloc/shuffile.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.0.3', sha256='6debdd9d6e6f1c4ec31015d7956e8b556acd61ce31f757e4d1fa5002029c75e2')

    depends_on('mpi')
    depends_on('kvtree')

    def cmake_args(self):
        args = []
        args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        if self.spec.satisfies('platform=cray'):
            args.append("-DSHUFFILE_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)
        return args
