# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys
from spack import *


class Tioga(CMakePackage, CudaPackage):
    """Topology Independent Overset Grid Assembly (TIOGA)"""

    homepage = "https://github.com/jsitaraman/tioga"
    git      = "https://github.com/jsitaraman/tioga.git"

    maintainers = ['jsitaraman', 'sayerhs']

    version('develop', branch='exawind')
    version('master', branch='master')

    variant('shared', default=sys.platform != 'darwin',
            description="Build shared libraries")
    variant('pic', default=True,
            description="Position independent code")
    variant('nodegid', default=True,
            description="Enable support for global Node IDs")
    variant('timers', default=False,
            description="Enable timers")
    variant('stats', default=False,
            description="Enable output of holecut stats")
    variant('cxxstd', default='11',
            values=('11', '14'), multi=False,
            description="C++ standard to use")

    depends_on('mpi')
    depends_on('cuda@9.0.0:', when='+cuda')

    # Tioga has the fortran module file problem with parallel builds
    parallel = False

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('CMAKE_POSITION_INDEPENDENT_CODE', 'pic'),
            self.define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
            self.define_from_variant('TIOGA_HAS_NODEGID', 'nodegid'),
            self.define_from_variant('TIOGA_ENABLE_TIMERS', 'timers'),
            self.define_from_variant('TIOGA_OUTPUT_STATS', 'stats'),
            self.define_from_variant('TIOGA_ENABLE_CUDA', 'cuda'),
        ]

        if '+cuda' in self.spec:
            args.append(self.define('CMAKE_CUDA_SEPARABLE_COMPILATION', True))

            # Currently TIOGA only supports one device arch during specialization
            cuda_arch = self.spec.variants['cuda_arch'].value
            if cuda_arch:
                arch_sorted = list(sorted(cuda_arch, reverse=True))
                args.append(self.define('TIOGA_CUDA_SM', arch_sorted[0]))

        if 'darwin' in spec.architecture:
            args.append(self.define('CMAKE_MACOSX_RPATH', True))

        return args
