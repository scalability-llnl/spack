# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qctool(WafPackage):
    """QCTOOL is a command-line utility program for manipulation and quality
    control of gwas datasets and other genome-wide data. This repository contains
    the source code for QCTOOL and a number of other command-line programs that
    manipulate gwas datasets and other genomic data, such as: Inthinnerator,
    HPTEST, and LDBIRD."""

    homepage = "https://www.chg.ox.ac.uk/~gav/qctool_v2/index.html"

    license("BSL-1.0")

    version(
        "2.2.0",
        sha256="7ba47998a2559193483cebe3710ce14d4e5d55d2e123840b4d1614b88459a9fc",
        url="https://enkre.net/cgi-bin/code/qctool/tarball/86639c1ad4/qctool-86639c1ad4.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Required external libraries as detailed in Prerequisites:
    # https://enkre.net/cgi-bin/code/qctool/wiki?name=Compiling+QCTOOL
    depends_on("zlib")
