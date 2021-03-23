# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack import *


class CBlosc(CMakePackage):
    """Blosc, an extremely fast, multi-threaded, meta-compressor library"""
    homepage = "http://www.blosc.org"
    url      = "https://github.com/Blosc/c-blosc/archive/v1.11.1.tar.gz"

    version('1.21.0', sha256='b0ef4fda82a1d9cbd11e0f4b9685abf14372db51703c595ecd4d76001a8b342d')
    version('1.17.0', sha256='75d98c752b8cf0d4a6380a3089d56523f175b0afa2d0cf724a1bd0a1a8f975a4')
    version('1.16.3', sha256='bec56cb0956725beb93d50478e918aca09f489f1bfe543dbd3087827a7344396')
    version('1.15.0', sha256='dbbb01f9fedcdf2c2ff73296353a9253f44ce9de89c081cbd8146170dce2ba8f')
    version('1.12.1', sha256='e04535e816bb942bedc9a0ba209944d1eb34e26e2d9cca37f114e8ee292cb3c8')
    version('1.11.1', sha256='d15937961d37b0780b8fb0641483eb9f6d4c379f88ac7ee84ff5dd06c2b72360')
    version('1.9.2',  sha256='6349ab927705a451439b2e23ec5c3473f6b7e444e6d4aafaff76b789713e9fee')
    version('1.9.1',  sha256='e4433fb0708517607cf4377837c4589807b9a8c112b94f7978cc8aaffb719bf0')
    version('1.9.0',  sha256='0cb5b5f7a25f71227e3dced7a6035e8ffd94736f7ae9fae546efa3b7c6e7a852')
    version('1.8.1',  sha256='1abf048634c37aeca53eeb6a9248ea235074077028d12b3560eccf1dff7143b8')
    version('1.8.0',  sha256='e0f8b9e12e86776a1b037385826c55006da6e2ae4973dac5b5ad3cfcf01e9043')

    variant('avx2', default=True, description='Enable AVX2 support')

    depends_on('cmake@2.8.10:', type='build')
    depends_on('snappy')
    depends_on('zlib')
    depends_on('zstd')
    depends_on('lz4')

    patch('gcc.patch', when="@1.12.1:1.17.0")
    patch('test_forksafe.patch', when='@1.15.0:1.17.0%intel')

    def cmake_args(self):
        args = []

        if '+avx2' in self.spec:
            args.append('-DDEACTIVATE_AVX2=OFF')
        else:
            args.append('-DDEACTIVATE_AVX2=ON')

        if self.spec.satisfies('@1.12.0:'):
            args.append('-DPREFER_EXTERNAL_SNAPPY=ON')
            args.append('-DPREFER_EXTERNAL_ZLIB=ON')
            args.append('-DPREFER_EXTERNAL_ZSTD=ON')
            args.append('-DPREFER_EXTERNAL_LZ4=ON')

            if self.run_tests:
                args.append('-DBUILD_TESTS=ON')
                args.append('-DBUILD_BENCHMARKS=ON')
            else:
                args.append('-DBUILD_TESTS=OFF')
                args.append('-DBUILD_BENCHMARKS=OFF')

        return args

    @run_after('install')
    def darwin_fix(self):
        if sys.platform == 'darwin':
            fix_darwin_install_name(self.prefix.lib)
