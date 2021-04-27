# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Er(CMakePackage):
    """Encoding and redundancy on a file set"""

    homepage = "https://github.com/ecp-veloc/er"
    url      = "https://github.com/ecp-veloc/er/archive/v0.0.3.tar.gz"
    git      = "https://github.com/ecp-veloc/er.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.0.4', sha256='c456d34719bb57774adf6d7bc2fa9917ecb4a9de442091023c931a2cb83dfd37')
    version('0.0.3', sha256='243b2b46ea274e17417ef5873c3ed7ba16dacdfdaf7053d1de5434e300de796b')

    depends_on('mpi')
    depends_on('kvtree+mpi')
    depends_on('rankstr', when='@0.0.4:')
    depends_on('redset')
    depends_on('shuffile')

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append("-DMPI_C_COMPILER=%s" % spec['mpi'].mpicc)
        if spec.satisfies('platform=cray'):
            args.append("-DER_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % spec['kvtree'].prefix)
        args.append("-DWITH_REDSET_PREFIX=%s" % spec['redset'].prefix)
        args.append("-DWITH_SHUFFILE_PREFIX=%s" % spec['shuffile'].prefix)
        if spec.satisfies('@0.0.4:'):
            args.append("-DWITH_RANKSTR_PREFIX=%s" % spec['rankstr'].prefix)
        return args
