# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Librsb(AutotoolsPackage):
    """librsb : A shared memory parallel sparse matrix computations
    library for the Recursive Sparse Blocks format"""

    homepage = "https://librsb.sourceforge.net/"
    url = "https://download.sourceforge.net/librsb/librsb-1.3.0.1.tar.gz"
    list_url = "https://sourceforge.net/projects/librsb/files/"

    license("LGPL-3.0-only")

    version("1.3.0.2", sha256="18c6fc443fa1cfd2a8110f7d4b88d5bbcb493b9e85b3a62014b8bb57a848e04f")
    version("1.3.0.1", sha256="3fc024a410f94aca2a7139ae79f4d713b11fa83304293630c363786874c17db4")
    version("1.3.0.0", sha256="2ac8725d1f988f57df9383ae6b0bb2ed221ec935187d31ebb62ea95ee868a790")
    version("1.2.0.11", sha256="0686be29bbe277e227c6021de6bd0564e4fc83f996b787886437d28048057bc8")
    version("1.2.0.10", sha256="ec49f3f78a7c43fc9e10976593d100aa49b1863309ed8fa3ccbb7aad52d2f7b8")
    version("1.2.0.9", sha256="f421f5d572461601120933e3c1cfee2ca69e6ecc92cbb11baa4e86bdedd3d9fa")
    version("1.2.0.8", sha256="8bebd19a1866d80ade13eabfdd0f07ae7e8a485c0b975b5d15f531ac204d80cb")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("zlib-api")
    depends_on("googletest", type="build", when="+googletest")
    conflicts("%apple-clang")
    # conflicts('%clang')
    conflicts("%gcc@11.0.0:11.2.99", msg="gcc-11.0:gcc-11.3 can break librsb on x86_64")
    conflicts("+asan", when="+native", msg="native must be disabled when asan is enabled")

    variant("asan", default=False, description="Use ASAN.")
    variant("debug", default=False, description="Enable debug features.")
    variant("googletest", default=False, description="Use Google Test as prerequisite.")
    variant("native", default=True, description="Use native flags.")
    variant("nospblas", default=False, description="Disable Building The Sparse BLAS API.")
    variant("serial", default=False, description="Disable OpenMP support.")
    variant("verbose", default=False, description="Extra Library Verbosity. Good for learning.")

    def setup_build_environment(self, spack_env):
        if self.spec.satisfies("+asan"):
            spack_env.set("LSAN_OPTIONS", "verbosity=1:log_threads=1")
            spack_env.set("ASAN_OPTS", "detect_leaks=0")

    def configure_args(self):
        args = [
            "--enable-openmp",
            "--with-zlib",
            "--enable-fortran-module-install",
            f"CPPFLAGS={self.spec['zlib-api'].headers.include_flags}",
            f"LDFLAGS={self.spec['zlib-api'].libs.search_flags}",
        ]
        if self.spec.satisfies("+asan"):
            args.append("CFLAGS=-O0 -ggdb -fsanitize=address -fno-omit-frame-pointer")
            args.append("CXXFLAGS=-O0 -ggdb -fsanitize=address -fno-omit-frame-pointer")
            args.append("LIBS=-lasan")
            args.append("FCLIBS=-lasan")
            args.append("--disable-shared")
            args.append("--enable-fortran-linker")
        if self.spec.satisfies("+debug"):
            args.append("--enable-allocator-wrapper")
            args.append("--enable-debug")
        if self.spec.satisfies("+native"):
            args.append("CFLAGS=-O3 -march=native")
            args.append("CXXFLAGS=-O3 -march=native")
            args.append("FCFLAGS=-O3 -march=native")
        if self.spec.satisfies("+nospblas"):
            args.append("--disable-sparse-blas-interface")
        if self.spec.satisfies("+serial"):
            args.append("--disable-openmp")
        if self.spec.satisfies("+verbose"):
            args.append("--enable-internals-error-verbosity=1")
            args.append("--enable-interface-error-verbosity=1")
        return args
