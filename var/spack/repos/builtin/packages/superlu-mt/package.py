# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class SuperluMt(Package):
    """SuperLU is a general purpose library for the direct solution of large,
    sparse, nonsymmetric systems of linear equations on high performance
    machines. SuperLU_MT is designed for shared memory parallel machines."""

    homepage = "https://crd-legacy.lbl.gov/~xiaoye/SuperLU/#superlu_mt"
    url = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_mt_3.1.tar.gz"
    git = "https://github.com/xiaoyeli/superlu_mt"

    version("master", branch="master")
    version("4.0.1", tag="v4.0.1", commit="1300aec2a46327ecdd34fc7460d56e86e5431f79")
    version("3.1", sha256="407b544b9a92b2ed536b1e713e80f986824cf3016657a4bfc2f3e7d2a76ecab6")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("int64", default=False, description="Build with 64 bit integers")
    variant("pic", default=True, description="Build with position independent code")
    variant("blas", default=True, description="Build with external BLAS library")

    # Must choose one or the other
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("pthread", default=True, description="Build with POSIX threads support")

    # NOTE: must link with a single-threaded BLAS library
    depends_on("blas", when="+blas")

    # Cannot be built in parallel
    parallel = False

    def configure(self, spec):
        # Validate chosen variants
        if "+openmp" in spec and "+pthread" in spec:
            msg = "You cannot choose both +openmp and +pthread"
            raise RuntimeError(msg)
        if "~openmp" in spec and "~pthread" in spec:
            msg = "You must choose either +openmp or +pthread"
            raise RuntimeError(msg)

        # List of configuration options
        config = []

        # The machine (platform) identifier to append to the library names
        if "+openmp" in spec:
            # OpenMP
            config.extend(
                [
                    "PLAT       = _OPENMP",
                    "TMGLIB     = libtmglib.a",
                    "MPLIB      = {0}".format(self.compiler.openmp_flag),
                    "CFLAGS     = {0}".format(self.compiler.openmp_flag),
                    "FFLAGS     = {0}".format(self.compiler.openmp_flag),
                    "LOADOPTS   += {0}".format(self.compiler.openmp_flag),
                ]
            )
        elif "+pthread" in spec:
            # POSIX threads
            config.extend(
                [
                    "PLAT       = _PTHREAD",
                    "TMGLIB     = libtmglib$(PLAT).a",
                    "MPLIB      = -lpthread",
                ]
            )

        # The BLAS library
        # NOTE: must link with a single-threaded BLAS library
        if "+blas" in spec:
            config.extend(
                [
                    "BLASDEF    = -DUSE_VENDOR_BLAS",
                    "BLASLIB    = {0}".format(spec["blas"].libs.ld_flags),
                ]
            )
        else:
            config.append("BLASLIB    = ../lib/libblas$(PLAT).a")

        # Generic options
        config.extend(
            [
                # The name of the libraries to be created/linked to
                "SUPERLULIB = libsuperlu_mt$(PLAT).a",
                "MATHLIB    = -lm",
                # The archiver and the flag(s) to use when building archives
                "ARCH       = ar",
                "ARCHFLAGS  = cr",
                "RANLIB     = {0}".format("ranlib" if which("ranlib") else "echo"),
                # Definitions used by CPP
                "PREDEFS    = -D_$(PLAT)",
                # Compilers and flags
                "CC         = {0}".format(os.environ["CC"]),
                "CFLAGS    += $(PREDEFS)",
                "NOOPTS     = -O0",
                "FORTRAN    = {0}".format(os.environ["FC"]),
                "LOADER     = {0}".format(os.environ["CC"]),
                # C preprocessor defs for compilation
                "CDEFS      = -DAdd_",
            ]
        )

        if "+int64" in spec:
            config.extend(["CFLAGS    += -D_LONGINT"])

        if "+pic" in spec:
            config.extend(
                [
                    "CFLAGS     += {0}".format(self.compiler.cc_pic_flag),
                    "NOOPTS     += {0}".format(self.compiler.cc_pic_flag),
                    "FFLAGS     += {0}".format(self.compiler.f77_pic_flag),
                    "LOADOPTS   += {0}".format(self.compiler.cc_pic_flag),
                ]
            )

        # Write configuration options to include file
        with open("make.inc", "w") as inc:
            for option in config:
                inc.write("{0}\n".format(option))

    def install(self, spec, prefix):
        # Set up make include file manually
        self.configure(spec)

        # Workaround Makefile bug where lib directory is not always created
        mkdirp("lib")

        # BLAS needs to be compiled separately if using internal BLAS library
        if "+blas" not in spec:
            make("blaslib")

        make()

        # Install manually
        install_tree("lib", prefix.lib)

        headers = glob.glob(join_path("SRC", "*.h"))
        mkdir(prefix.include)
        for h in headers:
            install(h, prefix.include)
