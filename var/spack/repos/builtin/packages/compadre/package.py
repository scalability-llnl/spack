# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Compadre(CMakePackage):
    """The Compadre Toolkit provides a performance portable solution for the
    parallel evaluation of computationally dense kernels. The toolkit
    specifically targets the Generalized Moving Least Squares (GMLS) approach,
    which requires the inversion of small dense matrices. The result is a set
    of weights that provide the information needed for remap or entries that
    constitute the rows of some globally sparse matrix.
    """

    homepage = 'https://github.com/SNLComputation/compadre'
    git      = 'https://github.com/SNLComputation/compadre.git'
    url      = 'https://github.com/SNLComputation/compadre/archive/v1.3.0.tar.gz'
    maintainers = ['kuberry']

    version('master',  branch='master', preferred=True)
    version('1.3.0', 'f711a840fd921e84660451ded408023ec3bcfc98fd0a7dc4a299bfae6ab489c2')

    depends_on('kokkos@3.3.01:main')
    depends_on('kokkos-kernels@3.3.01:main')
    depends_on('cmake@3.13:', type='build')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    variant('mpi', default=False, description='Enable MPI support')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec

        kokkos = spec['kokkos']
        kokkos_kernels = spec['kokkos-kernels']

        options = []
        options.extend([
            '-DKokkosCore_PREFIX={0}'.format(kokkos.prefix),
            '-DKokkosKernels_PREFIX={0}'.format(kokkos_kernels.prefix),
            '-DCMAKE_CXX_COMPILER:STRING={0}'.format(spec["kokkos"].kokkos_cxx),
        ])

        if '+mpi' in spec:
            options.append('-DCompadre_USE_MPI:BOOL=ON')

        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS:BOOL=OFF')

        return options
