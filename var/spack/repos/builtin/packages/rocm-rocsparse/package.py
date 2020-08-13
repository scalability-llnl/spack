# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmRocsparse(CMakePackage):
    """rocSPARSE exposes a common interface that provides Basic Linear
    Algebra Subroutines for sparse computation implemented on top of
    AMD's Radeon Open Compute ROCm runtime and toolchains. rocSPARSE
    is created using the HIP programming language and optimized for
    AMD's latest discrete GPUs."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSPARSE"
    url = "https://github.com/ROCmSoftwarePlatform/rocSPARSE/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', '9ca6bae7da78abbb47143c3d77ff4a8cd7d63979875fc7ebc46b400769fd9cb5')
    depends_on('rocm-hip-clang')
    depends_on('rocm-hip')
    depends_on('rocm-cmake')
    depends_on('rocm-rocprim')

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
        ]
        return cmake_args
