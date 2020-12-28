# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Er(CMakePackage):
    """Encoding and redundancy on a file set"""

    homepage = "https://github.com/ecp-veloc/er"
    url      = "https://github.com/ecp-veloc/er/archive/v0.0.3.zip"
    git      = "https://github.com/ecp-veloc/er.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.0.3', sha256='9aa08f9fe70e42f0da27a5d90d4643b520d61f24742303bf016322823b3c4d26')

    depends_on('mpi')
    depends_on('kvtree')
    depends_on('redset')
    depends_on('shuffile')

    def cmake_args(self):
        args = []
        args.append("-DMPI_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        if self.spec.satisfies('platform=cray'):
            args.append("-DER_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)
        args.append("-DWITH_REDSET_PREFIX=%s" % self.spec['redset'].prefix)
        args.append("-DWITH_SHUFFILE_PREFIX=%s" % self.spec['shuffile'].prefix)
        return args
