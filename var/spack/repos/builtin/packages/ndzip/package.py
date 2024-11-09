# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ndzip(CMakePackage, CudaPackage):
    """A High-Throughput Parallel Lossless Compressor for Scientific Data

    forked from: https://github.com/fknorr/ndzip
    """

    # the upstream developer graduated and moved on to other tasks

    url = "https://github.com/celerity/ndzip"
    homepage = "https://github.com/fknorr/ndzip"
    git = "https://github.com/robertu94/ndzip"

    maintainers("robertu94")

    license("MIT")

    version("master", branch="master")
    version("2021-11-30", commit="5b3c34991005c0924a339f2ec06750729ebbf015")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cuda", description="build with cuda support", default=False)
    variant("openmp", description="build with cuda support", default=False)

    depends_on("boost+thread+program_options")

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
