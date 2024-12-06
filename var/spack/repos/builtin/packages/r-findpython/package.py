# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFindpython(RPackage):
    """Package designed to find an acceptable python binary."""

    cran = "findpython"

    license("MIT")

    version("1.0.8", sha256="0f8a90cbafd4949c0333a86808383a358fb7ec3268953d8a4887d5d22264cdb7")
    version("1.0.7", sha256="59f904b9c2ec84b589380de59d13afbf14d1ec3b670e3a07e820298aaf04c149")
    version("1.0.5", sha256="3e9a21988cb78833769b02680d128a0cc01bcb41aa9c9725ab1742f349759145")
    version("1.0.4", sha256="a58fb46d53d3bdea1e00b2f4f9bdb5e98be9329ea9d8e2fe150d91462e6bccfd")
    version("1.0.3", sha256="5486535ae2f0a123b630d8eabf93a61b730765f55dfcc8ef4f6e56e7c49408f8")

    depends_on("python", type="run")
