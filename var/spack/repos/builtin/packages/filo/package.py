# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Filo(CMakePackage):
    """File flush and fetch, with MPI"""

    homepage = "https://github.com/ecp-veloc/filo"
    git      = "https://github.com/ecp-veloc/filo.git"

    tags = ['ecp']

    version('master', branch='master')

    depends_on('mpi')
    depends_on('axl')
    depends_on('kvtree')
    depends_on('spath')

    def cmake_args(self):
        args = []
        args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        if self.spec.satisfies('platform=cray'):
            args.append("-DFILO_LINK_STATIC=ON")
        args.append("-DWITH_AXL_PREFIX=%s" % self.spec['axl'].prefix)
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)
        args.append("-DWITH_SPATH_PREFIX=%s" % self.spec['spath'].prefix)
        return args
