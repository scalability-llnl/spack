# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CBlosc2(CMakePackage):
    """Next generation c-blosc with a new API, a new container and
       other bells and whistles"""

    homepage = "http://www.blosc.org"
    url      = "https://github.com/Blosc/c-blosc2/archive/refs/tags/v2.0.0.rc1.tar.gz"
    git      = "https://github.com/Blosc/c-blosc2.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('2.0.0.rc1', sha256='c30b72af5446f052bad1791000e5a44d156c96b0e39b4bc8e9f97a013c7d1b69')

    variant('avx2', default=True, description='Enable AVX2 support')

    variant('lizard', default=True,
            description='support for LIZARD (LZ5)')
    variant('lz4', default=True,
            description='support for LZ4')
    variant('snappy', default=True,
            description='support for SNAPPY')
    variant('zlib', default=True,
            description='support for ZLIB')
    variant('zstd', default=True,
            description='support for ZSTD')

    depends_on('cmake@2.8.10:', type='build')
    depends_on('lizard', when='+lizard')
    depends_on('lz4', when='+lz4')
    depends_on('snappy', when='+snappy')
    depends_on('zlib', when='+zlib')
    depends_on('zstd', when='+zstd')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DDEACTIVATE_LZ4={0}'.format(
                'ON' if '~lz4' in spec else 'OFF'),
            '-DDEACTIVATE_LIZARD={0}'.format(
                'ON' if '~lizard' in spec else 'OFF'),
            '-DDEACTIVATE_SNAPPY={0}'.format(
                'ON' if '~snappy' in spec else 'OFF'),
            '-DDEACTIVATE_ZLIB={0}'.format(
                'ON' if '~zlib' in spec else 'OFF'),
            '-DDEACTIVATE_ZSTD={0}'.format(
                'ON' if '~zstd' in spec else 'OFF'),
            '-DPREFER_EXTERNAL_LIZARD=ON',
            '-DPREFER_EXTERNAL_LZ4=ON',
            # snappy is supported via external install only
            '-DPREFER_EXTERNAL_ZLIB=ON',
            '-DPREFER_EXTERNAL_ZSTD=ON',
            '-DDEACTIVATE_AVX2={0}'.format(
                'ON' if '~avx2' in spec else 'OFF'),
            self.define('BUILD_TESTS', self.run_tests),
            self.define('BUILD_BENCHMARKS', self.run_tests),
            self.define('BUILD_EXAMPLES', self.run_tests)
        ]

        return args
