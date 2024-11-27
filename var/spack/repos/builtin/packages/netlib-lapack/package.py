# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.cmake
from spack.package import *


class NetlibLapack(CMakePackage):
    """LAPACK version 3.X is a comprehensive FORTRAN library that does
    linear algebra operations including matrix inversions, least squared
    solutions to linear sets of equations, eigenvector analysis, singular
    value decomposition, etc. It is a very comprehensive and reputable
    package that has found extensive use in the scientific community.

    """

    homepage = "https://www.netlib.org/lapack/"
    url = "https://www.netlib.org/lapack/lapack-3.5.0.tgz"
    tags = ["windows"]

    license("BSD-3-Clause-Open-MPI")

    version(
        "3.11.0",
        sha256="4b9ba79bfd4921ca820e83979db76ab3363155709444a787979e81c22285ffa9",
        url="https://github.com/Reference-LAPACK/lapack/archive/refs/tags/v3.11.0.tar.gz",
    )
    version(
        "3.10.1",
        sha256="cd005cd021f144d7d5f7f33c943942db9f03a28d110d6a3b80d718a295f7f714",
        url="https://github.com/Reference-LAPACK/lapack/archive/refs/tags/v3.10.1.tar.gz",
    )
    version(
        "3.10.0",
        sha256="328c1bea493a32cac5257d84157dc686cc3ab0b004e2bea22044e0a59f6f8a19",
        url="https://github.com/Reference-LAPACK/lapack/archive/refs/tags/v3.10.0.tar.gz",
    )
    version(
        "3.9.1",
        sha256="d0085d2caf997ff39299c05d4bacb6f3d27001d25a4cc613d48c1f352b73e7e0",
        url="https://github.com/Reference-LAPACK/lapack/archive/refs/tags/v3.9.1.tar.gz",
    )
    version(
        "3.9.0",
        sha256="106087f1bb5f46afdfba7f569d0cbe23dacb9a07cd24733765a0e89dbe1ad573",
        url="https://github.com/Reference-LAPACK/lapack/archive/v3.9.0.tar.gz",
    )
    version(
        "3.8.0",
        sha256="deb22cc4a6120bff72621155a9917f485f96ef8319ac074a7afbc68aab88bcf6",
        url="https://www.netlib.org/lapack/lapack-3.8.0.tar.gz",
    )
    version("3.7.1", sha256="f6c53fd9f56932f3ddb3d5e24c1c07e4cd9b3b08e7f89de9c867125eecc9a1c8")
    version("3.7.0", sha256="ed967e4307e986474ab02eb810eed1d1adc73f5e1e3bc78fb009f6fe766db3be")
    version("3.6.1", sha256="888a50d787a9d828074db581c80b2d22bdb91435a673b1bf6cd6eb51aa50d1de")
    version("3.6.0", sha256="a9a0082c918fe14e377bbd570057616768dca76cbdc713457d8199aaa233ffc3")
    version("3.5.0", sha256="9ad8f0d3f3fb5521db49f2dd716463b8fb2b6bc9dc386a9956b8c6144f726352")
    version("3.4.2", sha256="60a65daaf16ec315034675942618a2230521ea7adf85eea788ee54841072faf0")
    version("3.4.1", sha256="93b910f94f6091a2e71b59809c4db4a14655db527cfc5821ade2e8c8ab75380f")
    version("3.4.0", sha256="a7139ef97004d0e3c4c30f1c52d508fd7ae84b5fbaf0dd8e792c167dc306c3e9")
    version("3.3.1", sha256="56821ab51c29369a34e5085728f92c549a9aa926f26acf7eeac87b61eed329e4")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # netlib-lapack is the reference implementation of LAPACK
    for ver in [
        "3.10.1",
        "3.10.0",
        "3.9.1",
        "3.9.0",
        "3.8.0",
        "3.7.1",
        "3.7.0",
        "3.6.1",
        "3.6.0",
        "3.5.0",
        "3.4.2",
        "3.4.1",
        "3.4.0",
        "3.3.1",
    ]:
        provides("lapack@" + ver, when="@" + ver)

    variant("shared", default=True, description="Build shared library version")
    variant("pic", default=True, description="Produce position-independent code")
    variant("external-blas", default=False, description="Build lapack with an external blas")

    variant("lapacke", default=True, description="Activates the build of the LAPACKE C interface")
    variant("xblas", default=False, description="Builds extended precision routines using XBLAS")

    # Fixes for IBM XL and Cray CCE builds:
    #   Avoid optimizations that alter program semantics
    #   Don't assume fixed source form for Fortran
    #   Correct path to mangling config
    patch("ibm-xl.patch", when="@3.7:3.8 %xl")
    patch("ibm-xl.patch", when="@3.7:3.8 %xl_r")
    patch("ibm-xl.patch", when="@3.7:3.8 %cce@9:")

    # https://github.com/Reference-LAPACK/lapack/pull/621
    # Fixes for IBM XL and Cray CCE builds:
    #   Correct path to mangling config
    #   Fix logic for detecting recursive Fortran flags
    patch("ibm-xl-3.9.1.patch", when="@3.9.1 %xl")
    patch("ibm-xl-3.9.1.patch", when="@3.9.1 %xl_r")
    patch("ibm-xl-3.9.1.patch", when="@3.9.1 %cce@13:")

    # https://github.com/Reference-LAPACK/lapack/issues/228
    patch("undefined_declarations.patch", when="@3.8.0:3.8")

    # https://github.com/Reference-LAPACK/lapack/pull/268
    patch("testing.patch", when="@3.7.0:3.8")

    # liblapack links to libblas, so if this package is used as a lapack
    # provider, it must also provide blas.
    provides("lapack", "blas", when="~external-blas")
    provides("lapack")

    depends_on("blas", when="+external-blas")
    depends_on("netlib-xblas+fortran+plain_blas", when="+xblas")
    depends_on("python@2.7:", type="test")

    # We need to run every phase twice in order to get static and shared
    # versions of the libraries. When ~shared, we run the default
    # implementations of the CMakePackage's phases and get only one building
    # directory 'spack-build-static' with -DBUILD_SHARED_LIBS:BOOL=OFF (see
    # implementations of self.build_directory and self.cmake_args() below).
    # When +shared, we run the overridden methods for the phases, each
    # running the default implementation twice with different values for
    # self._building_shared. As a result, we get two building directories:
    # 'spack-build-static' with -DBUILD_SHARED_LIBS:BOOL=OFF and
    # 'spack-build-shared' with -DBUILD_SHARED_LIBS:BOOL=ON.
    _building_shared = False

    def patch(self):
        # Fix cblas CMakeLists.txt -- has wrong case for subdirectory name.
        if self.spec.satisfies("@3.6.0:"):
            filter_file(
                "${CMAKE_CURRENT_SOURCE_DIR}/CMAKE/",
                "${CMAKE_CURRENT_SOURCE_DIR}/cmake/",
                "CBLAS/CMakeLists.txt",
                string=True,
            )

        # Remove duplicate header file that gets generated during CMake shared
        # builds: https://github.com/Reference-LAPACK/lapack/issues/583
        if self.spec.satisfies("platform=windows @0:3.9.1"):
            force_remove("LAPACKE/include/lapacke_mangling.h")

    def xplatform_lib_name(self, lib):
        return (
            "lib" + lib
            if not lib.startswith("lib") and not self.spec.satisfies("platform=windows")
            else lib
        )

    @property
    def blas_libs(self):
        shared = "+shared" in self.spec
        query_parameters = self.spec.last_query.extra_parameters
        query2libraries = {
            tuple(): [self.xplatform_lib_name("blas")],
            ("c", "fortran"): [self.xplatform_lib_name("cblas"), self.xplatform_lib_name("blas")],
            ("c",): [self.xplatform_lib_name("cblas")],
            ("fortran",): [self.xplatform_lib_name("blas")],
        }
        key = tuple(sorted(query_parameters))
        libraries = query2libraries[key]
        return find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

    @property
    def lapack_libs(self):
        shared = True if "+shared" in self.spec else False
        query_parameters = self.spec.last_query.extra_parameters
        query2libraries = {
            tuple(): [self.xplatform_lib_name("lapack")],
            ("c", "fortran"): [
                self.xplatform_lib_name("lapacke"),
                self.xplatform_lib_name("lapack"),
            ],
            ("c",): [self.xplatform_lib_name("lapacke")],
            ("fortran",): [self.xplatform_lib_name("lapack")],
        }
        key = tuple(sorted(query_parameters))
        libraries = query2libraries[key]
        return find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

    @property
    def headers(self):
        include_dir = self.spec.prefix.include
        cblas_h = join_path(include_dir, "cblas.h")
        lapacke_h = join_path(include_dir, "lapacke.h")
        return HeaderList([cblas_h, lapacke_h])


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define_from_variant("LAPACKE", "lapacke"),
            self.define_from_variant("LAPACKE_WITH_TMG", "lapacke"),
            self.define("CBLAS", self.spec.satisfies("@3.6.0:")),
        ]

        if self.spec.satisfies("%intel"):
            # Intel compiler finds serious syntax issues when trying to
            # build CBLAS and LapackE
            args.extend([self.define("CBLAS", False), self.define("LAPACKE", False)])

        if self.spec.satisfies("%xl") or self.spec.satisfies("%xl_r"):
            # use F77 compiler if IBM XL
            args.extend(
                [
                    self.define("CMAKE_Fortran_COMPILER", self.pkg.compiler.f77),
                    self.define(
                        "CMAKE_Fortran_FLAGS",
                        " ".join(self.spec.compiler_flags["fflags"]) + " -O3 -qnohot",
                    ),
                ]
            )

        # deprecated routines are commonly needed by, for example, suitesparse
        # Note that OpenBLAS spack is built with deprecated routines
        args.append(self.define("BUILD_DEPRECATED", True))

        if self.spec.satisfies("+external-blas"):
            args.extend(
                [
                    self.define("USE_OPTIMIZED_BLAS", True),
                    self.define("BLAS_LIBRARIES:PATH", self.spec["blas"].libs.joined(";")),
                ]
            )

        if self.spec.satisfies("+xblas"):
            args.extend(
                [
                    self.define("XBLAS_INCLUDE_DIR", self.spec["netlib-xblas"].prefix.include),
                    self.define("XBLAS_LIBRARY", self.spec["netlib-xblas"].libs.joined(";")),
                ]
            )

        args.append(self.define("BUILD_TESTING", self.pkg.run_tests))

        return args
