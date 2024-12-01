# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Qrupdate(MakefilePackage, SourceforgePackage):
    """qrupdate is a Fortran library for fast updates of QR and
    Cholesky decompositions."""

    homepage = "https://sourceforge.net/projects/qrupdate/"
    sourceforge_mirror_path = "qrupdate/qrupdate-1.1.2.tar.gz"

    license("GPL-3.0-only")

    version("1.1.2", sha256="e2a1c711dc8ebc418e21195833814cb2f84b878b90a2774365f0166402308e08")

    depends_on("fortran", type="build")  # generated

    depends_on("blas")
    depends_on("lapack")

    def edit(self, spec, prefix):
        # BSD "install" does not understand GNU -D flag.
        # We will create the parent directory ourselves.
        if sys.platform == "darwin":
            makefile = FileFilter("src/Makefile")
            makefile.filter("-D", "")

        # Concurrent (parallel) Compilation requires calling $(MAKE) not make
        makefile = FileFilter("Makefile")
        makefile.filter("make", "$(MAKE)")

        # We may like to compile with any Forran compiler, not always gfortran
        makefile = FileFilter("Makeconf")
        makefile.filter("FC=gfortran", "FC ?= gfortran")

        return

    # The Makefile does not take the simple "make" rule
    def build(self, spec, prefix):
        lapack_blas = spec["lapack"].libs + spec["blas"].libs

        make_args = [
            "BLAS={0}".format(lapack_blas.ld_flags),
            "LAPACK={0}".format(lapack_blas.ld_flags),
        ]

        # If 64-bit BLAS is used:
        if (
            spec.satisfies("^openblas+ilp64")
            or spec.satisfies("^intel-mkl+ilp64")
            or spec.satisfies("^intel-parallel-studio+mkl+ilp64")
        ):
            if spec.satisfies("%intel") or spec.satisfies("%oneapi") or spec.satisfies("%nvhpc"):
                # 64bits integer for ifort and nvfortran are promoted by:
                make_args.append("FFLAGS=-i8")
            else:
                make_args.append("FFLAGS=-fdefault-integer-8")

        # Build static and dynamic libraries:
        make("lib", "solib", *make_args)

    def install(self, spec, prefix):
        # "INSTALL" confuses "make install" on case-insensitive filesystems:
        if os.path.isfile("INSTALL"):
            os.remove("INSTALL")

        # Create lib folder:
        if sys.platform == "darwin":
            mkdirp(prefix.lib)

        make("install", "PREFIX=%s" % prefix)

    @run_after("install")
    def fix_darwin_install(self):
        # The shared libraries are not installed correctly on Darwin:
        if sys.platform == "darwin":
            fix_darwin_install_name(self.spec.prefix.lib)
