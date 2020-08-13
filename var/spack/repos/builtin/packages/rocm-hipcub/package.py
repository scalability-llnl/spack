# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmHipcub(CMakePackage):
    """hipCUB is a thin wrapper library on top of rocPRIM or CUB. It
    enables developers to port project using CUB library to the HIP
    layer and to run them on AMD hardware. In ROCm environment hipCUB
    uses rocPRIM library as the backend, however, on CUDA platforms it
    uses CUB instead."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipCUB"
    url = "https://github.com/ROCmSoftwarePlatform/hipCUB/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', '1eb2cb5f6e90ed1b7a9ac6dd86f09ec2ea27bceb5a92eeffa9c2123950c53b9d')
    depends_on('rocm-hip-clang')
    depends_on('rocm-hip')
    depends_on('rocm-cmake')
    depends_on('rocm-rocprim')

    def patch(self):
        filter_file(r'find_package\(HIP 1\.5\.18263.*',
                    '',
                    'cmake/VerifyCompiler.cmake')

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
            "-DHIP_PLATFORM=hcc",
        ]
        return cmake_args
