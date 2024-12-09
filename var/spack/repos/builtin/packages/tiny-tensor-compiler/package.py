# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class TinyTensorCompiler(CMakePackage):
    """A compiler for tensor computations on GPUs and other devices,
    supporting the OpenCL, Level Zero, and SYCL runtime."""

    homepage = "https://github.com/intel/tiny-tensor-compiler"
    url = "https://github.com/intel/tiny-tensor-compiler/archive/refs/tags/v0.3.1.tar.gz"

    maintainers("uphoffc")

    license("BSD-3-Clause", checked_by="uphoffc")

    version("0.3.1", sha256="e512b92f9ef8f21362ea4a8f2655338769bc7fcf9de543e3dc7db86b696695b3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Shared library")
    variant("level-zero", default=False, description="Build tinytc_ze (Level Zero runtime)")
    variant("opencl", default=True, description="Build tintc_cl (OpenCL runtime)")
    variant("sycl", default=False, description="Build tinytc_sycl (SYCL runtime)")

    requires("+opencl +level-zero", when="+sycl")

    depends_on("cmake@3.23.0:", type="build")
    depends_on("double-batched-fft-library ~sycl ~level-zero ~opencl@0.5.1:", type="link")
    depends_on("oneapi-level-zero@1.13:", when="+level-zero")
    depends_on("opencl-c-headers@2022.01.04:", when="+opencl")
    depends_on("opencl-icd-loader@2022.01.04:", when="+opencl", type="link")
    depends_on("re2c@3.0:", type="build")
    depends_on("bison@3.8.2:", type="build")

    def cmake_args(self):
        cxx_compiler = os.path.basename(self.compiler.cxx)
        if self.spec.satisfies("+sycl") and cxx_compiler not in ["icpx"]:
            raise InstallError("The tinytc_sycl library requires the oneapi C++ compiler")

        return [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_SYCL", "sycl"),
            self.define_from_variant("BUILD_LEVEL_ZERO", "level-zero"),
            self.define_from_variant("BUILD_OPENCL", "opencl"),
        ]
