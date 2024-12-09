# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Dsdp(MakefilePackage):
    """The DSDP software is a free open source implementation of an
    interior-point method for semidefinite programming. It provides primal and
    dual solutions, exploits low-rank structure and sparsity in the data, and
    has relatively low memory requirements for an interior-point method. It
    allows feasible and infeasible starting points and provides approximate
    certificates of infeasibility when no feasible solution exists."""

    homepage = "https://www.mcs.anl.gov/hs/software/DSDP/"
    url = "https://www.mcs.anl.gov/hs/software/DSDP/DSDP5.8.tar.gz"

    license("DSDP")

    version("5.8", sha256="26aa624525a636de272c0b329e2dfd01a0d5b7827f1c1c76f393d71e37dead70")

    depends_on("c", type="build")  # generated

    depends_on("blas")
    depends_on("lapack")

    patch("malloc.patch")

    build_targets = ["dsdpapi"]

    def edit(self, spec, prefix):
        make_include = FileFilter("make.include")

        # STEP 1: Set DSDPROOT.
        make_include.filter("^#DSDPROOT.*=.*", "DSDPROOT = {0}".format(os.getcwd()))

        # STEP 2: Set the name of the C compiler.
        make_include.filter("^CC.*=.*", "CC = {0}".format(spack_cc))

        # STEP 5:
        # Location of BLAS AND LAPACK libraries.
        # Also include the math library and other libraries needed to
        # link the BLAS to the C files that call them.
        lapackblas = spec["lapack"].libs + spec["blas"].libs
        make_include.filter(
            "^LAPACKBLAS.*=.*", "LAPACKBLAS = {0}".format(lapackblas.link_flags + " -lm")
        )

    def install(self, spec, prefix):
        # Manual installation
        install_tree("lib", prefix.lib)
        install_tree("include", prefix.include)
