# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmHiprand(CMakePackage):
    """The rocRAND project provides functions that generate
    pseudo-random and quasi-random numbers. The rocRAND library is
    implemented in the HIP programming language and optimised for
    AMD's latest discrete GPUs. It is designed to run on top of AMD's
    Radeon Open Compute ROCm runtime, but it also works on CUDA
    enabled GPUs."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocRAND"
    url = "https://github.com/ROCmSoftwarePlatform/rocRAND/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', '592865a45e7ef55ad9d7eddc8082df69eacfd2c1f3e9c57810eb336b15cd5732')
    depends_on('rocm-hip')

    @property
    def headers(self):
        headers = find_all_headers(self.prefix)
        headers.directories = [self.prefix.hiprand.include,
                               self.prefix.rocrand.include]
        return headers

    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_CXX_COMPILER=hipcc",
        ]
        return cmake_args
