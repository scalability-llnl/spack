# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Shuffile(CMakePackage):
    """Shuffle files between MPI ranks"""

    homepage = "https://github.com/ecp-veloc/shuffile"
    url      = "https://github.com/ecp-veloc/shuffile/archive/v0.0.4.tar.gz"
    git      = "https://github.com/ecp-veloc/shuffile.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.0.4', sha256='f0249ab31fc6123103ad67b1eaf799277c72adcf0dfcddf8c3a18bad2d45031d')
    version('0.0.3', sha256='a3f685526a1146a5ad8dbacdc5f9c2e1152d9761a1a179c1db34f55afc8372f6')

    depends_on('mpi')
    depends_on('kvtree+mpi')

    def cmake_args(self):
        args = []
        args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        if self.spec.satisfies('platform=cray'):
            args.append("-DSHUFFILE_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)
        return args
