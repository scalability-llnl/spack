# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.blis import BlisBase


class Amdblis(BlisBase):
    """AMD Optimized BLIS.

    BLIS is a portable software framework for instantiating high-performance
    BLAS-like dense linear algebra libraries. The framework was designed to
    isolate essential kernels of computation that, when optimized, immediately
    enable optimized implementations of most of its commonly used and
    computationally intensive operations.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-BLIS license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/dense/eula/blas-4-2-eula.html
    https://www.amd.com/en/developer/aocl/dense/eula/blas-eula.html
    """

    _name = "amdblis"
    homepage = "https://www.amd.com/en/developer/aocl/blis.html"
    url = "https://github.com/amd/blis/archive/3.0.tar.gz"
    git = "https://github.com/amd/blis"

    maintainers("amd-toolchain-support")

    requires("target=x86_64:", msg="AMD blis available only on x86_64")

    license("BSD-3-Clause")

    version(
        "5.0",
        sha256="5abb34972b88b2839709d0af8785662bc651c7806ccfa41d386d93c900169bc2",
        preferred=True,
    )
    version("4.2", sha256="0e1baf850ba0e6f99e79f64bbb0a59fcb838ddb5028e24527f52b407c3c62963")
    version("4.1", sha256="a05c6c7d359232580d1d599696053ad0beeedf50f3b88d5d22ee7d34375ab577")
    version("4.0", sha256="cddd31176834a932753ac0fc4c76332868feab3e9ac607fa197d8b44c1e74a41")
    version("3.2", sha256="5a400ee4fc324e224e12f73cc37b915a00f92b400443b15ce3350278ad46fff6")
    version("3.1", sha256="2891948925b9db99eec02a1917d9887a7bee9ad2afc5421c9ba58602a620f2bf")
    version("3.0.1", sha256="dff643e6ef946846e91e8f81b75ff8fe21f1f2d227599aecd654d184d9beff3e")
    version("3.0", sha256="ac848c040cd6c3550fe49148dbdf109216cad72d3235763ee7ee8134e1528517")
    version("2.2", sha256="e1feb60ac919cf6d233c43c424f6a8a11eab2c62c2c6e3f2652c15ee9063c0c9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("ilp64", default=False, when="@3.0.1:", description="ILP64 support")
    variant("aocl_gemm", default=False, when="@4.1:", description="aocl_gemm support")
    variant("suphandling", default=True, description="Small Unpacked Kernel handling")

    variant("logging", default=False, description="Enable AOCL DTL Logging")
    variant("tracing", default=False, description="Enable AOCL DTL Tracing")

    def configure_args(self):
        spec = self.spec
        args = super().configure_args()

        if spec.satisfies("+ilp64"):
            args.append("--blas-int-size=64")

        if spec.satisfies("+aocl_gemm"):
            args.append("-a aocl_gemm")
            args.append("CC={0}".format(os.path.basename(spack_cc)))
            args.append("CXX={0}".format(os.path.basename(spack_cxx)))

        if spec.satisfies("+suphandling"):
            args.append("--enable-sup-handling")
        else:
            args.append("--disable-sup-handling")

        # To enable Fortran to C calling convention for
        # complex types when compiling with aocc flang
        if spec.satisfies("@3.0 %aocc"):
            args.append("CFLAGS={0}".format("-DAOCL_F2C"))
            args.append("CXXFLAGS={0}".format("-DAOCL_F2C"))
        elif spec.satisfies("@3.0.1: %aocc"):
            args.append("--complex-return=intel")

        if spec.satisfies("@3.1:"):
            args.append("--disable-aocl-dynamic")

        if spec.satisfies("+logging"):
            filter_file(
                "#define AOCL_DTL_LOG_ENABLE         0",
                "#define AOCL_DTL_LOG_ENABLE         1",
                f"{self.stage.source_path}/aocl_dtl/aocldtlcf.h",
            )

        if spec.satisfies("+tracing"):
            filter_file(
                "#define AOCL_DTL_TRACE_ENABLE       0",
                "#define AOCL_DTL_TRACE_ENABLE       1",
                f"{self.stage.source_path}/aocl_dtl/aocldtlcf.h",
            )

        return args

    @run_after("install")
    def create_symlink(self):
        with working_dir(self.prefix.lib):
            if os.path.isfile("libblis-mt.a"):
                os.symlink("libblis-mt.a", "libblis.a")
            if os.path.isfile("libblis-mt.so"):
                os.symlink("libblis-mt.so", "libblis.so")

    @property
    def libs(self):
        return find_libraries(
            ["libblis"] if self.spec.satisfies("threads=none") else ["libblis-mt"],
            root=self.prefix,
            shared=self.spec.satisfies("libs=shared"),
            recursive=True,
        )
