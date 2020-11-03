# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Chai(CMakePackage, CudaPackage):
    """
    Copy-hiding array interface for data migration between memory spaces
    """

    homepage = "https://github.com/LLNL/CHAI"
    git      = "https://github.com/LLNL/CHAI.git"

    version('develop', branch='develop', submodules='True')
    version('master', branch='main', submodules='True')
    version('2.1.1', tag='v2.1.1', submodules='True')
    version('2.1.0', tag='v2.1.0', submodules='True')
    version('2.0.0', tag='v2.0.0', submodules='True')
    version('1.2.0', tag='v1.2.0', submodules='True')
    version('1.1.0', tag='v1.1.0', submodules='True')
    version('1.0', tag='v1.0', submodules='True')

    variant('shared', default=True, description='Build Shared Libs')
    variant('raja', default=False, description='Build plugin for RAJA')
    variant('benchmarks', default=True, description='Build benchmarks.')
    variant('examples', default=True, description='Build examples.')

    depends_on('cmake@3.8:', type='build')
    depends_on('umpire')
    depends_on('raja', when="+raja")

    depends_on('cmake@3.9:', type='build', when="+cuda")
    depends_on('umpire+cuda', when="+cuda")
    depends_on('raja+cuda', when="+raja+cuda")

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=ON',
                '-DCUDA_TOOLKIT_ROOT_DIR=' + spec['cuda'].prefix])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                options.append('-DCMAKE_CUDA_FLAGS:STRING={0}'.format(flag))
        else:
            options.append('-DENABLE_CUDA=OFF')

        if '+raja' in spec:
            options.extend(['-DENABLE_RAJA_PLUGIN=ON',
                            '-DRAJA_DIR=' + spec['raja'].prefix])

        options.append('-Dumpire_DIR:PATH='
                       + spec['umpire'].prefix.share.umpire.cmake)

        options.append('-DENABLE_TESTS={0}'.format(
            'ON' if self.run_tests else 'OFF'))

        options.append('-DENABLE_BENCHMARKS={0}'.format(
            'ON' if '+benchmarks' in spec else 'OFF'))

        options.append('-DENABLE_EXAMPLES={0}'.format(
            'ON' if '+examples' in spec else 'OFF'))

        return options
