# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmMiopen(CMakePackage):
    """AMD's library for high performance machine learning primitives."""

    homepage = "https://github.com/ROCmSoftwarePlatform/MIOpen"
    url = "https://github.com/ROCmSoftwarePlatform/MIOpen/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', 'aa362e69c4dce7f5751f0ee04c745735ea5454c8101050e9b92cc60fa3c0fb82')
    depends_on('rocm-hip')
    depends_on('rocm-rocblas')
    depends_on('rocm-cmake')
    depends_on('rocm-clang-ocl')
    depends_on('sqlite')
    depends_on('boost@1.58:+pic')
    depends_on('half')
    depends_on('bzip2')

    def patch(self):
        filter_file(r'debug \$\{Boost_FILESYSTEM_LIBRARY_DEBUG\}',
                    '',
                    'src/CMakeLists.txt')
        filter_file(r'debug \$\{Boost_SYSTEM_LIBRARY_DEBUG\}',
                    '',
                    'src/CMakeLists.txt')
        filter_file(r'debug \$\{Boost_FILESYSTEM_LIBRARY_DEBUG\}',
                    '',
                    'speedtests/CMakeLists.txt')
        filter_file(r'debug \$\{Boost_SYSTEM_LIBRARY_DEBUG\}',
                    '',
                    'speedtests/CMakeLists.txt')
        filter_file(r'\$\{CLANG_TIDY_EXE\}',
                    '/bin/true',
                    'cmake/ClangTidy.cmake')

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
            "-DCLANG_TIDY_COMMAND=/bin/true",
        ]
        return cmake_args
