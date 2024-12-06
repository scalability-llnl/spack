# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class DoubleBatchedFftLibrary(CMakePackage):
    """A library for computing the Discrete Fourier Transform;
    targeting Graphics Processing Units; supporting OpenCL,
    Level Zero, and SYCL; with double-batching."""

    homepage = "https://github.com/intel/double-batched-fft-library"
    url = "https://github.com/intel/double-batched-fft-library/archive/refs/tags/v0.3.6.tar.gz"
    git = "https://github.com/intel/double-batched-fft-library.git"

    maintainers("uphoffc")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("develop", branch="develop")
    version("0.5.1", sha256="3651b982b6b5649d2bf95a3391a0a28d6637c51c642379d9708de88ad8d45f61")
    version("0.5.0", sha256="cbd2ecf039cc40830e57a8af8295abf2083ce3b1a333279a8c17762f41131fff")
    version("0.4.0", sha256="f3518012b632c92c2a933d70a040d6b0eee2d631ab6b1881a192a8d1624f242d")
    version("0.3.6", sha256="ff163251d77d3c686563141e871c702bf4997c0302d53616add55d6cf9b02d28")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Shared library")
    variant("sycl", default=True, description="Build bbfft-sycl")
    variant("level-zero", default=True, when="~sycl", description="Build bbfft-level-zero")
    variant("opencl", default=True, when="~sycl", description="Build bbfft-opencl")

    depends_on("cmake@3.23.0:", type="build")
    depends_on("oneapi-level-zero", when="+sycl")
    depends_on("oneapi-level-zero", when="+level-zero")
    depends_on("opencl", when="+opencl")

    patch("0001-Add-CPATH-and-LIBRARY_PATHs-to-OpenCL-search-paths.patch", when="@:0.3.6")

    def cmake_args(self):
        cxx_compiler = os.path.basename(self.compiler.cxx)
        if self.spec.satisfies("+sycl") and cxx_compiler not in ["icpx"]:
            raise InstallError("The Double-Batched FFT Library requires the oneapi C++ Compiler")

        return [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_SYCL", "sycl"),
            self.define_from_variant("BUILD_LEVEL_ZERO", "level-zero"),
            self.define_from_variant("BUILD_OPENCL", "opencl"),
            self.define("BUILD_BENCHMARK", False),
            self.define("BUILD_EXAMPLE", False),
            self.define("BUILD_TESTING", False),
        ]
