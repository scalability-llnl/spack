# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nvcomp(CMakePackage, CudaPackage):
    """Last open source release of A library for fast lossless compression
    /decompression on NVIDIA GPUs

    forked from: https://github.com/NVIDIA/nvcomp after NVIDIA made this closed source
    """

    homepage = "https://github.com/NVIDIA/nvcomp"
    url = "https://github.com/NVIDIA/nvcomp/archive/refs/tags/v2.0.2.tar.gz"

    # pinned to the last open source release+a few minor patches
    git = "https://github.com/robertu94/nvcomp"

    maintainers("robertu94")

    license("BSD-3-Clause")

    version("2.2.0", commit="3737f6e5028ed1887b0023ad0fc033e139d57574")
    version("2.0.2", commit="5d5c194f3449486d989057f632d10954b8d11d75")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cuda")
    conflicts("~cuda")

    def cmake_args(self):
        args = ["-DBUILD_EXAMPLES=OFF", "-DBUILD_BENCHMARKS=OFF"]
        cuda_arch_list = self.spec.variants["cuda_arch"].value
        args.append("CMAKE_CUDA_ARCHITECTURES={0}".format(";".join(cuda_arch_list)))
        return args
