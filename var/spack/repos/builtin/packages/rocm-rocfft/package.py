# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmRocfft(CMakePackage):
    """rocFFT is a software library for computing Fast Fourier
    Transforms (FFT) written in HIP. It is part of AMD's software
    ecosystem based on ROCm. In addition to AMD GPU devices, the
    library can also be compiled with the CUDA compiler using HIP
    tools for running on Nvidia GPU devices."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocFFT"
    url = "https://github.com/ROCmSoftwarePlatform/rocFFT/archive/3.5.0.tar.gz"

    version('3.5.0', '8e81701974c4c3b61b706aa805a50c7c7925d89e31f924b722e9f777bd2ae6d0')
    depends_on('rocm-hip')
    depends_on('rocm-cmake')

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
        ]
        return cmake_args
