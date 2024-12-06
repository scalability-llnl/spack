# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack.package import *


class Hpcg(AutotoolsPackage):
    """HPCG is a software package that performs a fixed number of multigrid
    preconditioned (using a symmetric Gauss-Seidel smoother) conjugate gradient
    (PCG) iterations using double precision (64 bit) floating point values."""

    homepage = "https://www.hpcg-benchmark.org"
    url = "https://www.hpcg-benchmark.org/downloads/hpcg-3.1.tar.gz"
    git = "https://github.com/hpcg-benchmark/hpcg.git"

    version("develop", branch="master")
    version("3.1", sha256="33a434e716b79e59e745f77ff72639c32623e7f928eeb7977655ffcaade0f4a4")

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Enable OpenMP support")

    patch(
        "https://github.com/hpcg-benchmark/hpcg/commit/e9e0b7e6cae23e1f30dd983c2ce2d3bd34d56f75.patch?full_index=1",
        sha256="722c13837b287e979442f8372274aa5910a290aa39f1ed1ff646116be08dcae9",
        when="%gcc@9:",
    )
    patch(
        "https://github.com/hpcg-benchmark/hpcg/commit/e9e0b7e6cae23e1f30dd983c2ce2d3bd34d56f75.patch?full_index=1",
        sha256="722c13837b287e979442f8372274aa5910a290aa39f1ed1ff646116be08dcae9",
        when="%aocc",
    )
    patch(
        "https://github.com/hpcg-benchmark/hpcg/commit/e9e0b7e6cae23e1f30dd983c2ce2d3bd34d56f75.patch?full_index=1",
        sha256="722c13837b287e979442f8372274aa5910a290aa39f1ed1ff646116be08dcae9",
        when="%arm",
    )
    patch(
        "https://github.com/hpcg-benchmark/hpcg/commit/e9e0b7e6cae23e1f30dd983c2ce2d3bd34d56f75.patch?full_index=1",
        sha256="722c13837b287e979442f8372274aa5910a290aa39f1ed1ff646116be08dcae9",
        when="%oneapi",
    )
    patch(
        "https://github.com/hpcg-benchmark/hpcg/commit/e9e0b7e6cae23e1f30dd983c2ce2d3bd34d56f75.patch?full_index=1",
        sha256="722c13837b287e979442f8372274aa5910a290aa39f1ed1ff646116be08dcae9",
        when="%intel",
    )
    patch(
        "https://github.com/hpcg-benchmark/hpcg/commit/e9e0b7e6cae23e1f30dd983c2ce2d3bd34d56f75.patch?full_index=1",
        sha256="722c13837b287e979442f8372274aa5910a290aa39f1ed1ff646116be08dcae9",
        when="%clang",
    )

    depends_on("mpi@1.1:")

    arch = "{0}-{1}".format(platform.system(), platform.processor())
    build_targets = ["arch={0}".format(arch)]

    def configure(self, spec, prefix):
        CXXFLAGS = "-O3 -ffast-math -ftree-vectorize "
        if (
            not spec.satisfies("%aocc")
            and not spec.satisfies("%cce")
            and not spec.satisfies("%arm")
            and not spec.satisfies("%intel")
            and not spec.satisfies("%oneapi")
            and not spec.satisfies("%clang")
        ):
            CXXFLAGS += " -ftree-vectorizer-verbose=0 "
        if spec.satisfies("%cce"):
            CXXFLAGS += " -Rpass=loop-vectorize"
            CXXFLAGS += " -Rpass-missed=loop-vectorize"
            CXXFLAGS += " -Rpass-analysis=loop-vectorize "
        if self.spec.satisfies("+openmp"):
            CXXFLAGS += self.compiler.openmp_flag
        config = [
            # Shell
            "SHELL         = /bin/sh",
            "CD            = cd",
            "CP            = cp",
            "LN_S          = ln -fs",
            "MKDIR         = mkdir -p",
            "RM            = /bin/rm -f",
            "TOUCH         = touch",
            # Platform identifier
            "ARCH          = {0}".format(self.arch),
            # HPCG Directory Structure / HPCG library
            "TOPdir        = {0}".format(os.getcwd()),
            "SRCdir        = $(TOPdir)/src",
            "INCdir        = $(TOPdir)/src",
            "BINdir        = $(TOPdir)/bin",
            # Message Passing library (MPI)
            "MPinc         = -I{0}".format(spec["mpi"].prefix.include),
            "MPlib         = -L{0}".format(spec["mpi"].prefix.lib),
            # HPCG includes / libraries / specifics
            "HPCG_INCLUDES = -I$(INCdir) -I$(INCdir)/$(arch) $(MPinc)",
            "HPCG_LIBS     =",
            "HPCG_OPTS     =",
            "HPCG_DEFS     = $(HPCG_OPTS) $(HPCG_INCLUDES)",
            # Compilers / linkers - Optimization flags
            "CXX           = {0}".format(spec["mpi"].mpicxx),
            "CXXFLAGS      = $(HPCG_DEFS) {0}".format(CXXFLAGS),
            "LINKER        = $(CXX)",
            "LINKFLAGS     = $(CXXFLAGS)",
            "ARCHIVER      = ar",
            "ARFLAGS       = r",
            "RANLIB        = echo",
        ]

        # Write configuration options to include file
        with open("setup/Make.{0}".format(self.arch), "w") as makefile:
            for var in config:
                makefile.write("{0}\n".format(var))

    def install(self, spec, prefix):
        # Manual installation
        install_tree("bin", prefix.bin)
