# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rankstr(CMakePackage):
    """Assign one-to-one mapping of MPI ranks to strings"""

    homepage = "https://github.com/ecp-veloc/rankstr"
    url      = "https://github.com/ecp-veloc/rankstr/archive/v0.0.2.zip"
    git      = "https://github.com/ecp-veloc/rankstr.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.0.2', sha256='c16d53aa9bb79934cbe2dcd8612e2db7d59de80be500c104e39e8623d4eacd8e')

    depends_on('mpi')

    def cmake_args(self):
        args = []
        args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        if self.spec.satisfies('platform=cray'):
            args.append("-DRANKSTR_LINK_STATIC=ON")
        return args
