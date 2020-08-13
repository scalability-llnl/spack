# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmClangOcl(CMakePackage):
    """OpenCL compilation with clang compiler."""

    homepage = "https://github.com/RadeonOpenCompute/clang-ocl"
    url = "https://github.com/RadeonOpenCompute/clang-ocl/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', '38c95fbd0ac3d11d9bd224ad333b68b9620dde502b8a8a9f3d96ba642901e8bb')
    depends_on('rocm-hip')
    depends_on('rocm-cmake')

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
        ]
        return cmake_args
