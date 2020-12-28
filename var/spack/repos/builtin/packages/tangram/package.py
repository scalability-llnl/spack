# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tangram(CMakePackage):
    """Tangram is an material interface reconstruction package used in
    multimaterial ALE codes and multi-material remapping
    (https://github.com/laristra/portage)
    """

    homepage = "https://portage.lanl.gov"
    git      = "https://github.com/laristra/tangram.git"
    url      = "https://github.com/laristra/tangram/releases/download/1.0.1/tangram-1.0.1.tar.gz"

    maintainers = ['raovgarimella']

    version('1.0.1', sha256='8f2f8c01bb2d726b0f64e5a5bc3aa2bd8057ccaee7a29c68f1439d16e39aaa90')
    version('master', branch='master', submodules=True)

    variant('mpi', default=True,
            description='Enable interface reconstruction with MPI')
    variant('thrust', default=False,
            description='Enable on-node parallelism with NVidia Thrust')
    variant('kokkos', default=False,
            description='Enable on-node or device parallelism with Kokkos')
    variant('openmp', default=False,
            description="Enable on-node parallelism using OpenMP")
    variant('cuda', default=False,
            description="Enable GPU parallelism using CUDA")

    # wrappers to enable external mesh/state libraries (only for testing)
    variant('jali', default=False,
            description='Build with Jali mesh infrastructure (for testing)')

    # Don't enable Kokkos and Thrust simultaneously
    conflicts('+jali~mpi')    # Jali needs MPI
    conflicts('+thrust +cuda')  # We don't have Thrust with CUDA working yet
    conflicts('+thrust +kokkos')  # Don't enable Kokkos, Thrust simultaneously

    # dependencies
    depends_on('cmake@3.13:', type='build')

    depends_on('mpi', when='+mpi')

    depends_on('wonton')
    depends_on('wonton+jali', when='+jali')
    depends_on('wonton~mpi', when='~mpi')
    depends_on('wonton+mpi', when='+mpi')
    depends_on('wonton+thrust', when='+thrust')
    depends_on('wonton+kokkos', when='+kokkos')
    depends_on('wonton+cuda', when='+cuda')
    depends_on('wonton+openmp', when='+openmp')
    depends_on('wonton+cuda', when='+cuda')

    def cmake_args(self):
        options = []
        if '+mpi' in self.spec:
            options.append('-DTANGRAM_ENABLE_MPI=ON')
        else:
            options.append('-DTANGRAM_ENABLE_MPI=OFF')

        if '+jali' in self.spec:
            options.append('-DTANGRAM_ENABLE_Jali=ON')
        else:
            options.append('-DTANGRAM_ENABLE_Jali=OFF')

        if '+thrust' in self.spec:
            options.append('-DTANGRAM_ENABLE_THRUST=ON')
        else:
            options.append('-DTANGRAM_ENABLE_THRUST=OFF')

        if '+kokkos' in self.spec:
            options.append('-DTANGRAM_ENABLE_Kokkos=ON')
        else:
            options.append('-DTANGRAM_ENABLE_Kokkos=OFF')

        # Unit test variant
        if self.run_tests:
            options.append('-DENABLE_UNIT_TESTS=ON')
            options.append('-DENABLE_APP_TESTS=ON')
        else:
            options.append('-DENABLE_UNIT_TESTS=OFF')
            options.append('-DENABLE_APP_TESTS=OFF')

        return options
