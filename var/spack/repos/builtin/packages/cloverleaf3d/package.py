# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Cloverleaf3d(MakefilePackage):
    """Proxy Application. CloverLeaf3D is 3D version of the
       CloverLeaf mini-app. CloverLeaf is a mini-app that solves
       the compressible Euler equations on a Cartesian grid,
       using an explicit, second-order accurate method.
    """

    homepage = "http://uk-mac.github.io/CloverLeaf3D/"
    url      = "http://downloads.mantevo.org/releaseTarballs/miniapps/CloverLeaf3D/CloverLeaf3D-1.0.tar.gz"

    tags = ['proxy-app']

    version('1.0', sha256='78d591728c61bdfd6175b3930df7652e09ed04fbcd01b3fc86fb2aa0f237a8ef')

    variant('openacc', default=False, description='Enable OpenACC Support')

    depends_on('mpi')

    @property
    def type_of_build(self):
        build = 'ref'

        if '+openacc' in self.spec:
            build = 'OpenACC'

        return build

    @property
    def build_targets(self):
        targets = [
            'MPI_COMPILER={0}'.format(self.spec['mpi'].mpifc),
            'C_MPI_COMPILER={0}'.format(self.spec['mpi'].mpicc),
            '--directory=CloverLeaf3D_{0}'.format(self.type_of_build)
        ]

        if '%gcc' in self.spec:
            targets.append('COMPILER=GNU')
            targets.append('FLAGS_GNU=')
            targets.append('CFLAGS_GNU=')
        elif '%cce' in self.spec:
            targets.append('COMPILER=CRAY')
            targets.append('FLAGS_CRAY=')
            targets.append('CFLAGS_CRAY=')
        elif '%intel' in self.spec:
            targets.append('COMPILER=INTEL')
            targets.append('FLAGS_INTEL=')
            targets.append('CFLAGS_INTEL=')
        elif '%pgi' in self.spec:
            targets.append('COMPILER=PGI')
            targets.append('FLAGS_PGI=')
            targets.append('CFLAGS_PGI=')
        elif '%xl' in self.spec:
            targets.append('COMPILER=XLF')
            targets.append('FLAGS_XLF=')
            targets.append('CFLAGS_XLF=')

        return targets

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc.samples)

        install('README.md', prefix.doc)

        install('CloverLeaf3D_{0}/clover_leaf'.format(self.type_of_build),
                prefix.bin)
        install('CloverLeaf3D_{0}/clover.in'.format(self.type_of_build),
                prefix.bin)
        install('CloverLeaf3D_{0}/*.in'.format(self.type_of_build),
                prefix.doc.samples)
