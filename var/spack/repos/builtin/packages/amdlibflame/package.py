# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------\

import spack.build_systems.autotools
import spack.build_systems.cmake
from spack.package import *
from spack.pkg.builtin.libflame import LibflameBase


class Amdlibflame(CMakePackage, LibflameBase):
    """libFLAME (AMD Optimized version) is a portable library for
    dense matrix computations, providing much of the functionality
    present in Linear Algebra Package (LAPACK). It includes a
    compatibility layer, FLAPACK, which includes complete LAPACK
    implementation.

    The library provides scientific and numerical computing communities
    with a modern, high-performance dense linear algebra library that is
    extensible, easy to use, and available under an open source
    license. libFLAME is a C-only implementation and does not
    depend on any external FORTRAN libraries including LAPACK.
    There is an optional backward compatibility layer, lapack2flame
    that maps LAPACK routine invocations to their corresponding
    native C implementations in libFLAME. This allows legacy
    applications to start taking advantage of libFLAME with
    virtually no changes to their source code.

    In combination with BLIS library which includes optimizations
    for the AMD EPYC processor family, libFLAME enables running
    high performing LAPACK functionalities on AMD platform.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-libFLAME license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/dense/eula-libflame/libflame-4-2-eula.html
    https://www.amd.com/en/developer/aocl/dense/eula-libflame/libflame-eula.html
    """

    _name = "amdlibflame"
    homepage = "https://www.amd.com/en/developer/aocl/blis.html#libflame"
    url = "https://github.com/amd/libflame/archive/3.0.tar.gz"
    git = "https://github.com/amd/amdlibflame"

    maintainers("amd-toolchain-support")

    license("BSD-3-Clause")

    version(
        "5.0",
        sha256="3bee3712459a8c5bd728a521d8a4c8f46735730bf35d48c878d2fc45fc000918",
        preferred=True,
    )
    version("4.2", sha256="93a433c169528ffba74a99df0ba3ce3d5b1fab9bf06ce8d2fd72ee84768ed84c")
    version("4.1", sha256="8aed69c60d11cc17e058cabcb8a931cee4f343064ade3e73d3392b7214624b61")
    version("4.0", sha256="bcb05763aa1df1e88f0da5e43ff86d956826cbea1d9c5ff591d78a3e091c66a4")
    version("3.2", sha256="6b5337fb668b82d0ed0a4ab4b5af4e2f72e4cedbeeb4a8b6eb9a3ef057fb749a")
    version("3.1", sha256="4520fb93fcc89161f65a40810cae0fa1f87cecb242da4a69655f502545a53426")
    version("3.0.1", sha256="5859e7b39ffbe73115dd598b035f212d36310462cf3a45e555a5087301710776")
    version("3.0", sha256="d94e08b688539748571e6d4c1ec1ce42732eac18bd75de989234983c33f01ced")
    version("2.2", sha256="12b9c1f92d2c2fa637305aaa15cf706652406f210eaa5cbc17aaea9fcfa576dc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("ilp64", default=False, when="@3.0.1: ", description="Build with ILP64 support")
    variant(
        "vectorization",
        default="auto",
        when="@4.2:",
        values=("auto", "avx2", "avx512", "none"),
        multi=False,
        description="Use hardware vectorization support",
    )

    variant("logging", default="False", description="Enable AOCL DTL Logging")
    variant("tracing", default="False", description="Enable AOCL DTL Tracing")

    # Build system
    build_system(
        conditional("cmake", when="@4.2:"), conditional("autotools", when="@:4.1"), default="cmake"
    )

    # Required dependencies
    with when("build_system=cmake"):
        generator("make")
        depends_on("cmake@3.22:", type="build")

    conflicts("threads=pthreads", msg="pthread is not supported")
    conflicts("threads=openmp", when="@:3", msg="openmp is not supported by amdlibflame < 4.0")
    requires("target=x86_64:", msg="AMD libflame available only on x86_64")

    patch("aocc-2.2.0.patch", when="@:2", level=1)
    patch("cray-compiler-wrapper.patch", when="@:3.0.0", level=1)
    patch("supermat.patch", when="@4.0:4.1", level=1)
    patch("libflame-pkgconfig.patch", when="@4.2")

    provides("flame@5.2", when="@2:")

    depends_on("python+pythoncmd", type="build")
    depends_on("gmake@4:", when="@3.0.1,3.1:", type="build")

    for vers in ["4.1", "4.2", "5.0"]:
        with when(f"@{vers}"):
            depends_on(f"aocl-utils@{vers}")

    @property
    def lapack_libs(self):
        """find lapack_libs function"""
        return find_libraries(
            "libflame", root=self.prefix, shared="+shared" in self.spec, recursive=True
        )

    @property
    def libs(self):
        """find libflame libs function"""
        return find_libraries(
            "libflame", root=self.prefix, shared="+shared" in self.spec, recursive=True
        )

    def flag_handler(self, name, flags):
        if name == "cflags":
            if (
                self.spec.satisfies("%clang@16:")
                or self.spec.satisfies("%aocc@4.1.0:")
                or self.spec.satisfies("%gcc@14:")
            ):
                flags.append("-Wno-implicit-function-declaration")
            if self.spec.satisfies("%clang@16:") or self.spec.satisfies("%aocc@4.1.0:"):
                flags.append("-Wno-error=incompatible-function-pointer-types")
                flags.append("-Wno-sometimes-uninitialized")
        if name == "ldflags":
            if self.spec.satisfies("^aocl-utils~shared"):
                flags.append("-lstdc++")
        return (flags, None, None)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        args = [self.define("LIBAOCLUTILS_INCLUDE_PATH", spec["aocl-utils"].prefix.include)]
        aocl_utils_lib_path = spec["aocl-utils"].libs
        args.append("-DLIBAOCLUTILS_LIBRARY_PATH={0}".format(aocl_utils_lib_path))
        # From 3.2 version, amd optimized flags are encapsulated under:
        # ENABLE_AMD_AOCC_FLAGS for AOCC compiler
        # ENABLE_AMD_FLAGS for all other compilers
        if spec.satisfies("@3.2:"):
            if spec.satisfies("%aocc"):
                args.append(self.define("ENABLE_AMD_AOCC_FLAGS", True))
            else:
                args.append(self.define("ENABLE_AMD_FLAGS", True))

        if spec.satisfies("threads=none"):
            args.append(self.define("ENABLE_MULTITHREADING", False))

        if spec.satisfies("@3.0.1: +ilp64"):
            args.append(self.define("ENABLE_ILP64", True))

        if spec.satisfies("@4.2: ^[virtuals=blas] amdblis"):
            args.append(self.define("ENABLE_AOCL_BLAS", True))
            args.append("-DAOCL_ROOT:PATH={0}".format(spec["blas"].prefix))

        if spec.variants["vectorization"].value == "auto":
            if spec.satisfies("target=avx512"):
                args.append("-DLF_ISA_CONFIG=avx512")
            elif spec.satisfies("target=avx2"):
                args.append("-DLF_ISA_CONFIG=avx2")
            else:
                args.append("-DLF_ISA_CONFIG=none")
        else:
            args.append(self.define("LF_ISA_CONFIG", spec.variants["vectorization"].value))

        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        return args


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        """configure_args function"""
        args = self.pkg.configure_args()
        spec = self.spec

        # From 3.2 version, amd optimized flags are encapsulated under:
        # enable-amd-aocc-flags for AOCC compiler
        # enable-amd-flags for all other compilers
        if spec.satisfies("@3.2: "):
            if spec.satisfies("%aocc"):
                args.append("--enable-amd-aocc-flags")
            else:
                args.append("--enable-amd-flags")

        if spec.satisfies("@:3.1"):
            args.append("--enable-external-lapack-interfaces")

        if spec.satisfies("@3.1"):
            args.append("--enable-blas-ext-gemmt")

        if spec.satisfies("@3.1 %aocc"):
            args.append("--enable-void-return-complex")

        if spec.satisfies("@3.0:3.1 %aocc"):
            """To enabled Fortran to C calling convention for
            complex types when compiling with aocc flang"""
            args.append("--enable-f2c-dotc")

        if spec.satisfies("@3.0.1: +ilp64"):
            args.append("--enable-ilp64")

        if spec.satisfies("@4.1:"):
            args.append("CFLAGS=-I{0}".format(spec["aocl-utils"].prefix.include))
            aocl_utils_lib_path = spec["aocl-utils"].libs
            args.append("LIBAOCLUTILS_LIBRARY_PATH={0}".format(aocl_utils_lib_path))

        if spec.satisfies("+tracing"):
            filter_file(
                "#define AOCL_DTL_TRACE_ENABLE       0",
                "#define AOCL_DTL_TRACE_ENABLE       1",
                f"{self.stage.source_path}/aocl_dtl/aocldtlcf.h",
            )

        if spec.satisfies("+logging"):
            filter_file(
                "#define AOCL_DTL_LOG_ENABLE         0",
                "#define AOCL_DTL_LOG_ENABLE         1",
                f"{self.stage.source_path}/aocl_dtl/aocldtlcf.h",
            )

        return args

    @when("@4.1:")
    def build(self, pkg, spec, prefix):
        aocl_utils_lib_path = spec["aocl-utils"].libs
        make("all", "LIBAOCLUTILS_LIBRARY_PATH={0}".format(aocl_utils_lib_path))

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check(self):
        """make check for single and multithread"""
        blas_flags = self.spec["blas"].libs.ld_flags
        if self.spec.variants["threads"].value != "none":
            make("check", "LIBBLAS = -fopenmp {0}".format(blas_flags), parallel=False)
        else:
            make("check", "LIBBLAS = {0}".format(blas_flags), parallel=False)

    def install(self, pkg, spec, prefix):
        """make install function"""
        # make install in parallel fails with message 'File already exists'
        make("install", parallel=False)

    def setup_dependent_run_environment(self, env, dependent_spec):
        if self.spec.external:
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
