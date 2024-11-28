# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bgen(WafPackage):
    """This repository contains a reference implementation of the BGEN format, written
    in C++. The library can be used as the basis for BGEN support in other software,
    or as a reference for developers writing their own implementations of the BGEN format.

    If you make use of the BGEN library, its tools or example programs, please cite:

    Band, G. and Marchini, J., "BGEN: a binary file format for imputed genotype and
    haplotype data", bioArxiv 308296; doi: https://doi.org/10.1101/308296."""

    homepage = "https://enkre.net/cgi-bin/code/bgen"

    license("BSL-1.0")

    version(
        "1.1.7",
        sha256="121f5956f04ad174bc410fa7deed59e2ebff0ec818a3c66cf5d667357dddfb62",
        url="https://enkre.net/cgi-bin/code/bgen/tarball/6ac2d582f9/BGEN-6ac2d582f9.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
