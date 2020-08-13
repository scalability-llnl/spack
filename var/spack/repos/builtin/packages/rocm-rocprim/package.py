# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmRocprim(CMakePackage):
    """The rocPRIM is a header-only library providing HIP parallel
    primitives for developing performant GPU-accelerated code on AMD
    ROCm platform."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocPRIM"
    url = "https://github.com/ROCmSoftwarePlatform/rocPRIM/archive/rocm-3.5.0.tar.gz"

    version('3.5.1', '12b2220303562976dd2557506728e3b250167215e500cfd446fe7ebe0022f9f2')
    version('3.5.0', '29302dbeb27ae88632aa1be43a721f03e7e597c329602f9ca9c9c530c1def40d')
    depends_on('rocm-hip-clang')
    depends_on('rocm-hip')
    depends_on('rocm-cmake')

    def patch(self):
        filter_file(r'find_package\(HIP 1\.5\.18263.*',
                    '',
                    'cmake/VerifyCompiler.cmake')

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
            "-DHIP_PLATFORM=clang",
        ]
        return cmake_args
