# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zfp(CMakePackage):
    """zfp is an open source C/C++ library for high-fidelity, high-throughput
       lossy compression of floating-point and integer multi-dimensional
       arrays.
    """

    homepage = 'http://computing.llnl.gov/projects/floating-point-compression'
    url      = 'http://computing.llnl.gov/projects/floating-point-compression/download/zfp-0.5.2.tar.gz'

    version('0.5.5', sha256='fdf7b948bab1f4e5dccfe2c2048fd98c24e417ad8fb8a51ed3463d04147393c5')
    version('0.5.4', sha256='768a05ed9bf10e54ac306f90b81dd17b0e7b13782f01823d7da4394fd2da8adb')
    version('0.5.2', sha256='89e718edb966422b5898b5c37b1b0a781d4effacb511520558469e3ff7f65d7c')
    version('0.5.1', sha256='867c04cf965f1c70d9725b396c6e1b5d29db55b0d69b8e87a995aaebd221b830')

    variant('bsws',
            default='64',
            values=('8', '16', '32', '64'),
            multi=False,
            description='Bit stream word size: use smaller for finer '
            'rate granularity. Use 8 for H5Z-ZFP filter.')
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
    variant('shared', default=True,
            description='Build shared versions of the library')

    depends_on('cmake@3.4.0:', type='build')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DZFP_BIT_STREAM_WORD_SIZE:STRING={0}'.format(
                spec.variants['bsws'].value),
            '-DZFP_WITH_BIT_STREAM_STRIDED:BOOL={0}'.format(
                'ON' if '+strided' in spec else 'OFF'),
            '-DZFP_WITH_ALIGNED_ALLOC:BOOL={0}'.format(
                'ON' if '+aligned' in spec else 'OFF'),
            '-DZFP_WITH_CACHE_TWOWAY:BOOL={0}'.format(
                'ON' if '+twoway' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF')
        ]
        if spec.version >= Version('0.5.2'):
            args.append('-DZFP_WITH_CACHE_FAST_HASH:BOOL={0}'.format(
                'ON' if '+fasthash' in spec else 'OFF'))
            args.append('-DZFP_WITH_CACHE_PROFILE:BOOL={0}'.format(
                'ON' if '+profile' in spec else 'OFF'))

        return args
