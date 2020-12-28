# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Benchmark(CMakePackage):
    """A microbenchmark support library"""

    homepage = "https://github.com/google/benchmark"
    url      = "https://github.com/google/benchmark/archive/v1.1.0.tar.gz"
    git      = "https://github.com/google/benchmark.git"

    # first properly installed CMake config packages in
    # 1.2.0 release: https://github.com/google/benchmark/issues/363

    version('develop', branch='master')
    version('1.5.0', sha256='3c6a165b6ecc948967a1ead710d4a181d7b0fbcaa183ef7ea84604994966221a')
    version('1.4.1', sha256='f8e525db3c42efc9c7f3bc5176a8fa893a9a9920bbd08cef30fb56a51854d60d')
    version('1.4.0', sha256='616f252f37d61b15037e3c2ef956905baf9c9eecfeab400cb3ad25bae714e214')
    version('1.3.0', sha256='f19559475a592cbd5ac48b61f6b9cedf87f0b6775d1443de54cfe8f53940b28d')
    version('1.2.0', sha256='3dcc90c158838e2ac4a7ad06af9e28eb5877cf28252a81e55eb3c836757d3070')
    version('1.1.0', sha256='e7334dd254434c6668e33a54c8f839194c7c61840d52f4b6258eee28e9f3b20e')
    version('1.0.0', sha256='d2206c263fc1a7803d4b10e164e0c225f6bcf0d5e5f20b87929f137dee247b54')

    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'MinSizeRel', 'Coverage'))

    depends_on("cmake@2.8.11:", type="build", when="@:1.1.0")
    depends_on("cmake@2.8.12:", type="build", when="@1.2.0:1.4")
    depends_on("cmake@3.5.1:",  type="build", when="@1.5.0:")

    def cmake_args(self):
        # No need for testing for the install
        args = ["-DBENCHMARK_ENABLE_TESTING=OFF"]
        return args

    def patch(self):
        filter_file(
            r'add_cxx_compiler_flag..fstrict.aliasing.',
            r'##### add_cxx_compiler_flag(-fstrict-aliasing)',
            'CMakeLists.txt'
        )
        filter_file(
            r'add_cxx_compiler_flag..Werror',
            r'##### add_cxx_compiler_flag(-Werror',
            'CMakeLists.txt'
        )
