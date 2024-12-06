# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qnnpack(CMakePackage):
    """QNNPACK (Quantized Neural Networks PACKage) is a mobile-optimized
    library for low-precision high-performance neural network inference.
    QNNPACK provides implementation of common neural network operators on
    quantized 8-bit tensors."""

    homepage = "https://github.com/pytorch/QNNPACK"
    git = "https://github.com/pytorch/QNNPACK.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2019-08-28", commit="7d2a4e9931a82adc3814275b6219a03e24e36b4c")  # py-torch@1.3:1.9
    version("2018-12-27", commit="6c62fddc6d15602be27e9e4cbb9e985151d2fa82")  # py-torch@1.2
    version("2018-12-04", commit="ef05e87cef6b8e719989ce875b5e1c9fdb304c05")  # py-torch@1.0:1.1

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    generator("ninja")
    depends_on("cmake@3.5:", type="build")
    depends_on("python", type="build")

    resource(
        name="cpuinfo",
        git="https://github.com/Maratyszcza/cpuinfo.git",
        destination="deps",
        placement="cpuinfo",
    )
    resource(
        name="fp16",
        git="https://github.com/Maratyszcza/FP16.git",
        destination="deps",
        placement="fp16",
    )
    resource(
        name="fxdiv",
        git="https://github.com/Maratyszcza/FXdiv.git",
        destination="deps",
        placement="fxdiv",
    )
    resource(
        name="googlebenchmark",
        url="https://github.com/google/benchmark/archive/v1.4.1.zip",
        sha256="61ae07eb5d4a0b02753419eb17a82b7d322786bb36ab62bd3df331a4d47c00a7",
        destination="deps",
        placement="googlebenchmark",
    )
    resource(
        name="googletest",
        url="https://github.com/google/googletest/archive/release-1.8.0.zip",
        sha256="f3ed3b58511efd272eb074a3a6d6fb79d7c2e6a0e374323d1e6bcbcc1ef141bf",
        destination="deps",
        placement="googletest",
    )
    resource(
        name="psimd",
        git="https://github.com/Maratyszcza/psimd.git",
        destination="deps",
        placement="psimd",
    )
    resource(
        name="pthreadpool",
        git="https://github.com/Maratyszcza/pthreadpool.git",
        destination="deps",
        placement="pthreadpool",
    )

    def cmake_args(self):
        return [
            self.define(
                "CPUINFO_SOURCE_DIR", join_path(self.stage.source_path, "deps", "cpuinfo")
            ),
            self.define("FP16_SOURCE_DIR", join_path(self.stage.source_path, "deps", "fp16")),
            self.define("FXDIV_SOURCE_DIR", join_path(self.stage.source_path, "deps", "fxdiv")),
            self.define("PSIMD_SOURCE_DIR", join_path(self.stage.source_path, "deps", "psimd")),
            self.define(
                "PTHREADPOOL_SOURCE_DIR", join_path(self.stage.source_path, "deps", "pthreadpool")
            ),
            self.define(
                "GOOGLEBENCHMARK_SOURCE_DIR",
                join_path(self.stage.source_path, "deps", "googlebenchmark"),
            ),
            self.define(
                "GOOGLETEST_SOURCE_DIR", join_path(self.stage.source_path, "deps", "googletest")
            ),
            self.define("QNNPACK_BUILD_TESTS", self.run_tests),
            self.define("QNNPACK_BUILD_BENCHMARKS", self.run_tests),
        ]
