# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class IqTree(CMakePackage):
    """IQ-TREE Efficient software for phylogenomic inference"""

    homepage = "http://www.iqtree.org"
    git      = "https://github.com/Cibiv/IQ-TREE.git"
    url      = "https://github.com/Cibiv/IQ-TREE/archive/v1.6.12.tar.gz"

    version('2.0.6',    tag='v2.0.6', submodules=True)
    version('1.6.12',   sha256='9614092de7a157de82c9cc402b19cc8bfa0cb0ffc93b91817875c2b4bb46a284')

    variant('openmp', default=True, description='Enable OpenMP support.')
    variant('mpi',    default=False, description='Enable MPI support.')
    variant('lsd2',   default=True,  description='Axctivate Least Squares Dating.')

    maintainers = ['ilbiondo']

    # Depends on Eigen3 and zlib

    depends_on("boost")
    depends_on("eigen")
    depends_on("zlib")
    depends_on('mpi', when='+mpi')

    def cmake_args(self):

        spec = self.spec
        args = []
        iqflags = []

        if '+lsd2' in spec:
            args.append('-DUSE_LSD2=ON')

        if '+openmp' in spec:
            iqflags.append('omp')

        if '+mpi' in spec:
            iqflags.append('mpi')

        if not iqflags:
            iqflags.append('single')

        args.append('-DIQTREE_FLAGS=' + ",".join(iqflags))

        return args
