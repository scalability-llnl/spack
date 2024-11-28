# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPng(RPackage):
    """Read and write PNG images.

    This package provides an easy and simple way to read, write and display
    bitmap images stored in the PNG format. It can read and write both files
    and in-memory raw vectors."""

    cran = "png"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("0.1-8", sha256="5a36fabb6d62ba2533d3fc4cececd07891942cfb76fe689ec0d550d08762f61c")
    version("0.1-7", sha256="e269ff968f04384fc9421d17cfc7c10cf7756b11c2d6d126e9776f5aca65553c")

    depends_on("c", type="build")  # generated

    depends_on("r@2.9.0:", type=("build", "run"))
    depends_on("libpng")
