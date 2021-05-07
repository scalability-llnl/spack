# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zfp(CMakePackage, CudaPackage):
    """zfp is a compressed number format for multidimensional floating-point
       and integer arrays.

       zfp provides compressed-array classes that support high throughput
       read and write random access to individual array elements. zfp also
       supports serial and parallel (OpenMP and CUDA) compression of whole
       arrays.
    """

    # Package info
    homepage    = 'https://zfp.llnl.gov'
    url         = 'https://github.com/LLNL/zfp/releases/download/0.5.5/zfp-0.5.5.tar.gz'
    git         = 'https://github.com/LLNL/zfp.git'
    maintainers = ['lindstro', 'GarrettDMorrison']

    # Versions
    version('develop', branch='develop')
    version('0.5.5', sha256='fdf7b948bab1f4e5dccfe2c2048fd98c24e417ad8fb8a51ed3463d04147393c5')
    version('0.5.4', sha256='746e17aaa401c67dcffd273d6e6f95c76adfbbd5cf523dcad56d09e9d3b71196')
    version('0.5.3', sha256='a5d2f8e5b47a7c92e2a5775b82cbfb3a76c87d0ac83d25abb4ac10ea75a2856e')
    version('0.5.2', sha256='9c738ec525cc76b4bb80b2b3f7c9f07507eeda3a341470e5942cda97efbe9a4f', url='https://github.com/LLNL/zfp/archive/0.5.2/zfp-0.5.2.tar.gz')
    version('0.5.1', sha256='f255dd1708c9ae4dc6a56dd2614e8b47a10d833c87fd349cbd47545a19c2b779', url='https://github.com/LLNL/zfp/archive/0.5.1/zfp-0.5.1.tar.gz')

    # Build targets
    # TODO: variant('utilities', default=True,  description='Build utilities')
    variant('shared',    default=True,  description='Build shared libraries')

    # Language bindings
    variant('c',       default=False, description='Enable C bindings')
    variant('python',  default=False, description='Enable Python bindings')
    variant('fortran', default=False, description='Enable Fortran bindings')

    # Execution policies
    variant('openmp', default=False, description='Enable OpenMP execution')
    variant('cuda',   default=False, description='Enable CUDA execution')

    # Advanced options
    variant('bsws', default='64', values=('8', '16', '32', '64'), multi=False,
            description='Bit stream word size: '
            'use smaller for finer rate granularity. '
            'Use 8 for H5Z-ZFP filter.')
    variant('strided', default=False,
            description='Enable strided access for progressive zfp streams')
    variant('aligned', default=False,
            description='Enable aligned memory allocation')
    variant('twoway', default=False,
            description='Use two-way skew-associative cache')
    variant('fasthash', default=False,
            description='Use a faster but more collision prone hash function')
    variant('profile', default=False,
            description='Count cache misses')

    # Conflicts
    conflicts('+c',        when='@:0.5.3',
              msg='+c requires zfp 0.5.4 or later')
    conflicts('+python',   when='@:0.5.4',
              msg='+python requires zfp 0.5.5 or later')
    conflicts('+fortran',  when='@:0.5.4',
              msg='+fortran requires zfp 0.5.5 or later')
    conflicts('+openmp',   when='@:0.5.2',
              msg='+openmp requires zfp 0.5.3 or later')
    conflicts('+cuda',     when='@:0.5.3',
              msg='+cuda requires zfp 0.5.4 or later')
    conflicts('+fasthash', when='@:0.5.1',
              msg='+fasthash requires zfp 0.5.2 or later')
    conflicts('+profile',  when='@:0.5.1',
              msg='+profile requires zfp 0.5.2 or later')

    # Dependencies
    depends_on('cmake@3.4.0:', type='build')
    depends_on('cuda@7:',      type=('build', 'test', 'run'), when='+cuda')
    depends_on('python',     type=('build', 'test', 'run'), when='+python')
    depends_on('py-numpy',     type=('build', 'test', 'run'), when='+python')
    depends_on('py-cython',    type='build',                  when='+python')

    def cmake_args(self):
        spec = self.spec

        # CMake options
        args = [
            # TODO: self.define_from_variant('BUILD_UTILITIES', 'utilities'),
            self.define('BUILD_TESTING', self.run_tests),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('BUILD_CFP', 'c'),
            self.define_from_variant('BUILD_ZFPY', 'python'),
            self.define_from_variant('BUILD_ZFORP', 'fortran'),
            self.define('ZFP_BIT_STREAM_WORD_SIZE',
                        spec.variants['bsws'].value),
            self.define_from_variant('ZFP_WITH_BIT_STREAM_STRIDED', 'strided'),
            self.define_from_variant('ZFP_WITH_ALIGNED_ALLOC', 'aligned'),
            self.define_from_variant('ZFP_WITH_CACHE_TWOWAY', 'twoway'),
            self.define_from_variant('ZFP_WITH_CACHE_FAST_HASH', 'fasthash'),
            self.define_from_variant('ZFP_WITH_CACHE_PROFILE', 'profile')
        ]

        return args
