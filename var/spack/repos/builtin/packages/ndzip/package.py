# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ndzip(CMakePackage, CudaPackage):
    """A High-Throughput Parallel Lossless Compressor for Scientific Data"""

    url = "https://github.com/celerity/ndzip"
    homepage = "https://github.com/fknorr/ndzip"
    git = "https://github.com/robertu94/ndzip"

    maintainers = ["robertu94"]

    version("master", branch="master")

    variant("cuda", description="build with cuda support", default=False)
    variant("openmp", description="build with cuda support", default=False)

    def cmake_args(self):
        args = [
            self.define_from_variant("NDZIP_WITH_CUDA", "cuda"),
            self.define_from_variant("NDZIP_WITH_MT", "openmp"),
            self.define("NDZIP_BUILD_BENCHMARK", False),
            self.define("NDZIP_BUILD_TEST", self.run_tests),
            self.define("NDZIP_USE_WERROR", False),
        ]
        if "+cuda" in self.spec and self.spec.variants["cuda_arch"].value != "none":
            arch_str = ";".join(self.spec.variants["cuda_arch"].value)
            args.append(self.define("CMAKE_CUDA_ARCHITECTURES", arch_str))
        return args
