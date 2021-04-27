# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Redset(CMakePackage):
    """Create MPI communicators for disparate redundancy sets"""

    homepage = "https://github.com/ecp-veloc/redset"
    url      = "https://github.com/ecp-veloc/redset/archive/v0.0.5.tar.gz"
    git      = "https://github.com/ecp-veloc/redset.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.0.5', sha256='4db4ae59ab9d333a6d1d80678dedf917d23ad461c88b6d39466fc4bf6467d1ee')
    version('0.0.4', sha256='c33fce458d5582f01ad632c6fae8eb0a03eaef00e3c240c713b03bb95e2787ad')
    version('0.0.3', sha256='30ac1a960f842ae23a960a88b312af3fddc4795f2053eeeec3433a61e4666a76')

    depends_on('mpi')
    depends_on('rankstr')
    depends_on('kvtree+mpi')

    def cmake_args(self):
        args = []
        args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        if self.spec.satisfies('platform=cray'):
            args.append("-DREDSET_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)
        args.append("-DWITH_RANKSTR_PREFIX=%s" % self.spec['rankstr'].prefix)
        return args
