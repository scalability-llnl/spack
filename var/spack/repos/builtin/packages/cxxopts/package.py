# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cxxopts(CMakePackage):
    """Lightweight C++ command line option parser"""

    homepage = "https://github.com/jarro2783/cxxopts"
    url      = "https://github.com/jarro2783/cxxopts/archive/v2.2.0.tar.gz"

    version('2.2.0', sha256='447dbfc2361fce9742c5d1c9cfb25731c977b405f9085a738fbd608626da8a4d')
    version('2.1.2', sha256='95f524c6615a2067e935e02ef74b013b17efa339df0a3c9db3e91fc0afbaf269')
    version('2.1.1', sha256='e19216251427d04f0273e6487c0246ae2dbb4154bf178f43896af8fa1ef89f3f')
    version('2.1.0', sha256='7672c79e5e48dd0cb1935c6efe65d2695d96fa764bf06c493d2db25a3cf633b4')
    version('2.0.0', sha256='f575a12645743032c27a7bc661e8598f249a8453d7f5388bcae66ac3b089399e')
    version('1.4.4', sha256='1d0eedb39ecbc64a0f82d8b6fe40d5c8e611501702969cfbd14a07ce6ddb8501')
    version('1.4.3', sha256='9103d6d75a3f599728256ce89922a8cd348bfe5874de62ca1436f605f194c52e')
    version('1.4.2', sha256='8fc5e16e68ddf549465f8bec6b56adaccfab9d183093616ddd4d3e80115844cb')
    version('1.4.1', sha256='c5ccfe99bd3db0604d077c968b39a42d61333a64d171fe84d7037d6c0dcc996d')
    version('1.4.0', sha256='60d4a482ec603ef4efa2603978596716884b33e24d39af6ddca52b4a30f7107b')

    variant('unicode', default=False,
            description='Enables unicode support using the ICU library.')

    depends_on('cmake@3.1.0:', type='build')
    depends_on('icu4c', when='+unicode')

    def cmake_args(self):
        args = ['-DCXXOPTS_ENABLE_INSTALL=ON',
                '-DCXXOPTS_BUILD_EXAMPLES=OFF',
                '-DCXXOPTS_BUILD_TESTS=OFF']

        if '+unicode' in self.spec:
            args.append('-DCXXOPTS_USE_UNICODE_HELP=ON')
        else:
            args.append('-DCXXOPTS_USE_UNICODE_HELP=OFF')

        return args
