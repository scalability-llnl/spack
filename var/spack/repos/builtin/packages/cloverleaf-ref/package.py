# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CloverleafRef(MakefilePackage):
    """Proxy Application. CloverLeaf_ref is a miniapp that solves the
    compressible Euler equations on a Cartesian grid,
    using an explicit, second-order accurate method.
    """

    homepage = "https://github.com/UK-MAC/CloverLeaf_ref"
    url = "https://github.com/UK-MAC/CloverLeaf_ref/archive/refs/tags/v1.3.tar.gz"
    git = "https://github.com/UK-MAC/CloverLeaf_ref.git"

    maintainers("amd-toolchain-support")

    version("master", branch="master")
    version(
        "1.3", sha256="fdff193286a00672bb931baa50d424a2cc19fb5817b62436804eced637e12430"
    )  # commit "0ddf495"
    version(
        "1.1", sha256="0ac87accf81d85b959e5da839e6b0659afb3a2840a13f5da113a1c34eeb87942"
    )  # commit "5667c3a"

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "ieee", default=False, description="Build with IEEE754 compliant floating point operations"
    )
    variant("debug", default=False, description="Build with DEBUG flags")

    depends_on("mpi")

    # Cloverleaf_ref Makefile contains some but not all required options for each compiler.
    # This package.py inserts what is needed for Intel, AOCC, and LLVM compilers.
    @property
    def build_targets(self):
        targets = ["--directory=./"]

        targets.append("MPI_COMPILER={0}".format(self.spec["mpi"].mpifc))
        targets.append("C_MPI_COMPILER={0}".format(self.spec["mpi"].mpicc))

        if self.spec.satisfies("+debug"):
            targets.append("DEBUG=1")
        if self.spec.satisfies("+ieee"):
            targets.append("IEEE=1")

        # Work around for bug in Makefiles for versions 1.3 and 1.1 (mis-defined as -openmp)
        if self.spec.satisfies("%intel"):
            targets.append("COMPILER=INTEL")
            targets.append("OMP_INTEL=-qopenmp")

        # Work around for missing AOCC compilers option in Makefiles for versions 1.3 and 1.1
        elif self.spec.satisfies("%aocc"):
            targets.append("COMPILER=AOCC")
            targets.append("OMP_AOCC=-fopenmp")

            if self.spec.satisfies("+ieee"):
                targets.append("I3E_AOCC=-ffp-model=precise")
                if self.spec.satisfies("%aocc@:4.0.0"):
                    targets.append("I3E_AOCC+=-Kieee")

            # logic for Debug build: no optimizatrion and debug symbols
            if self.spec.satisfies("+debug"):
                targets.append("FLAGS_AOCC=-O0 -g -Wall -Wextra -fsanitize=address")
                targets.append("CFLAGS_AOCC=-O0 -g -Wall -Wextra -fsanitize=address")
            else:
                targets.append("CFLAGS_AOCC=-O3 -fnt-store=aggressive")
                targets.append("FLAGS_AOCC=-O3 -fnt-store=aggressive")

        # Work around for missing CLANG entries in Makefiles for master branch (commit:0fdb917),
        # and for versions 1.3 and 1.1
        elif self.spec.satisfies("%clang"):
            targets.append("COMPILER=CLANG")
            targets.append("OMP_CLANG=-fopenmp")

            if self.spec.satisfies("+ieee"):
                targets.append("I3E_CLANG=-ffp-model=precise")

            # logic for Debug build: no optimizatrion and debug symbols
            if self.spec.satisfies("+debug"):
                targets.append("FLAGS_CLANG=-O0 -g")
                targets.append("CFLAGS_CLANG=-O0 -g")
            else:
                targets.append("FLAGS_CLANG=-O3")
                targets.append("CFLAGS_CLANG=-O3")

        elif self.spec.satisfies("%gcc"):
            targets.append("COMPILER=GNU")

        elif self.spec.satisfies("%cce"):
            targets.append("COMPILER=CRAY")
            targets.append("OMP_CRAY=-fopenmp")

        elif self.spec.satisfies("%xl"):
            targets.append("COMPILER=XLF")

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.doc.tests)

        install("./clover_leaf", prefix.bin)
        install("./clover.in", prefix.bin)
        install("./*.in", prefix.doc.tests)
