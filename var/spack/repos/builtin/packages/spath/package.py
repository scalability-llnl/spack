# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spath(CMakePackage):
    """Represent and manipulate file system paths"""

    homepage = "https://github.com/ecp-veloc/spath"
    git      = "https://github.com/ecp-veloc/spath.git"

    tags = ['ecp']

    version('master', branch='master')

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
