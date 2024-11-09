# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NetlibXblas(AutotoolsPackage):
    """XBLAS is a reference implementation for extra precision BLAS.

    XBLAS is a reference implementation for the dense and banded BLAS
    routines, along with extended and mixed precision version. Extended
    precision is only used internally; input and output arguments remain
    the same as in the existing BLAS. Extra precisions is implemented as
    double-double (i.e., 128-bit total, 106-bit significand). Mixed
    precision permits some input/output arguments of different types
    (mixing real and complex) or precisions (mixing single and
    double). This implementation is proof of concept, and no attempt was
    made to optimize performance; performance should be as good as
    straightforward but careful code written by hand."""

    homepage = "https://www.netlib.org/xblas"
    url = "https://www.netlib.org/xblas/xblas.tar.gz"

    license("BSD-3-Clause")

    version("1.0.248", sha256="b5fe7c71c2da1ed9bcdc5784a12c5fa9fb417577513fe8a38de5de0007f7aaa1")

    depends_on("c", type="build")
    depends_on("m4", type="build")

    variant("fortran", default=True, description="Build Fortran interfaces")
    variant("plain_blas", default=True, description="As part of XBLAS, build plain BLAS routines")

    provides("blas", when="+plain_blas")

    @property
    def libs(self):
        return find_libraries(["libxblas"], root=self.prefix, shared=False, recursive=True)

    def configure_args(self):
        args = []

        if self.spec.satisfies("~fortran"):
            args += ["--disable-fortran"]

        if self.spec.satisfies("~plain_blas"):
            args += ["--disable-plain-blas"]

        return args

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        install("libxblas.a", prefix.lib)

        if self.spec.satisfies("+plain_blas"):
            # XBLAS should be a drop-in BLAS replacement
            install("libxblas.a", join_path(prefix.lib, "libblas.a"))

        headers = [
            "f2c-bridge.h",
            "blas_dense_proto.h",
            "blas_enum.h",
            "blas_extended.h",
            "blas_extended_private.h",
            "blas_extended_proto.h",
            "blas_fpu.h",
            "blas_malloc.h",
        ]
        mkdirp(prefix.include)
        for h in headers:
            install(join_path("src", h), prefix.include)

        return
