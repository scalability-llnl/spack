# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Arrow(CMakePackage, CudaPackage):
    """A cross-language development platform for in-memory data.

    This package contains the C++ bindings.
    """

    homepage = "http://arrow.apache.org"
    url      = "https://github.com/apache/arrow/archive/apache-arrow-0.9.0.tar.gz"

    version('0.17.1', sha256='ecb6da20f9288c0ca31f9b457ffdd460198765a8af27c1cac4b1382a8d130f86')
    version('0.15.1', sha256='ab1c0d371a10b615eccfcead71bb79832245d788f4834cc6b278c03c3872d593')
    version('0.15.0', sha256='d1072d8c4bf9166949f4b722a89350a88b7c8912f51642a5d52283448acdfd58')
    version('0.14.1', sha256='69d9de9ec60a3080543b28a5334dbaf892ca34235b8bd8f8c1c01a33253926c1')
    version('0.12.1', sha256='aae68622edc3dcadaa16b2d25ae3f00290d5233100321993427b03bcf5b1dd3b')
    version('0.11.0', sha256='0ac629a7775d86108e403eb66d9f1a3d3bdd6b3a497a86228aa4e8143364b7cc')
    version('0.9.0', sha256='65f89a3910b6df02ac71e4d4283db9b02c5b3f1e627346c7b6a5982ae994af91')
    version('0.8.0', sha256='c61a60c298c30546fc0b418a35be66ef330fb81b06c49928acca7f1a34671d54')

    depends_on('boost@1.60:')
    depends_on('cmake@3.2.0:', type='build')
    depends_on('flatbuffers build_type=Release')  # only Release contains flatc
    depends_on('python', when='+python')
    depends_on('py-numpy', when='+python')
    depends_on('rapidjson')
    depends_on('snappy~shared')
    depends_on('zlib+pic')
    depends_on('zstd+pic')
    depends_on('thrift+pic', when='+parquet')
    depends_on('orc', when='+orc')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'FastDebug', 'Release'))
    variant('python', default=False, description='Build Python interface')
    variant('parquet', default=False, description='Build Parquet interface')
    variant('orc', default=False, description='Build ORC support')

    root_cmakelists_dir = 'cpp'

    def patch(self):
        """Prevent `-isystem /usr/include` from appearing, since this confuses gcc.
        """
        filter_file(r'(include_directories\()SYSTEM ',
                    r'\1',
                    'cpp/cmake_modules/ThirdpartyToolchain.cmake')

    def cmake_args(self):
        args = [
            "-DARROW_USE_SSE=ON",
            "-DARROW_BUILD_SHARED=ON",
            "-DARROW_BUILD_STATIC=OFF",
            "-DARROW_BUILD_TESTS=OFF",
            "-DARROW_WITH_BROTLI=OFF",
            "-DARROW_WITH_LZ4=OFF",
        ]

        if self.spec.satisfies('+cuda'):
            args.append('-DARROW_CUDA:BOOL=ON')
        else:
            args.append('-DARROW_CUDA:BOOL=OFF')

        if self.spec.satisfies('+python'):
            args.append("-DARROW_PYTHON:BOOL=ON")
        else:
            args.append('-DARROW_PYTHON:BOOL=OFF')

        if self.spec.satisfies('+parquet'):
            args.append("-DARROW_PARQUET:BOOL=ON")
        else:
            args.append("-DARROW_PARQUET:BOOL=OFF")

        if self.spec.satisfies('+orc'):
            args.append('-DARROW_ORC:BOOL=ON')
        else:
            args.append('-DARROW_ORC:BOOL=OFF')

        for dep in ('flatbuffers', 'rapidjson', 'snappy', 'zlib', 'zstd'):
            args.append("-D{0}_HOME={1}".format(dep.upper(),
                                                self.spec[dep].prefix))
        args.append("-DZLIB_LIBRARIES={0}".format(self.spec['zlib'].libs))
        return args
