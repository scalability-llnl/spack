# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xsimd(CMakePackage):
    """C++ wrappers for SIMD intrinsics"""

    homepage = "http://quantstack.net/xsimd"
    url      = "https://github.com/QuantStack/xsimd/archive/3.1.0.tar.gz"
    git      = "https://github.com/QuantStack/xsimd.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('7.4.10', sha256='df00f476dea0c52ffebad60924e3f0db2a016b80d508f8d5a2399a74c0d134cd')
    version('7.4.9', sha256='f6601ffb002864ec0dc6013efd9f7a72d756418857c2d893be0644a2f041874e')
    version('7.2.3', sha256='bbc673ad3e9d4523503a4222da05886e086b0e0bd6bd93d03ea3b663c74297b9')
    version('4.0.0', sha256='67b818601c15ef15ea4d611a8cd7382588c340ebd9146c799a0210d212540455')
    version('3.1.0', sha256='d56288826f6b82fd9583f83ace6aa2306ba2ae82cec003de1d04ce17fbb1e91f')

    depends_on('googletest', type='test')

    # C++14 support
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.6')
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')

    def cmake_args(self):
        args = [
            '-DBUILD_TESTS:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF')
        ]

        return args
