# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Redset(CMakePackage):
    """Create MPI communicators for disparate redundancy sets"""

    homepage = "https://github.com/ecp-veloc/redset"
    url      = "https://github.com/ecp-veloc/redset/archive/v0.0.3.zip"
    git      = "https://github.com/ecp-veloc/redset.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.0.3', sha256='f110c9b42209d65f84a8478b919b27ebe2d566839cb0cd0c86ccbdb1f51598f4')

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
