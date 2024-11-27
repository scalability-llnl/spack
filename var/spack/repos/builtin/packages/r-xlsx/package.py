# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXlsx(RPackage):
    """Read, Write, Format Excel 2007 and Excel 97/2000/XP/2003 Files.

    Provide R functions to read/write/format Excel 2007 and Excel
    97/2000/XP/2003 file formats."""

    cran = "xlsx"

    license("GPL-3.0-only")

    version("0.6.5", sha256="378c5ed475a3d7631ea1ea13e0a69d619c1a52260922abda42818752dbb32107")
    version("0.6.1", sha256="a580bd16b5477c1c185bf681c12c1ffff4088089f97b6a37997913d93ec5a8b4")

    depends_on("r-rjava", type=("build", "run"))
    depends_on("r-xlsxjars", type=("build", "run"))
    depends_on("java@6:")
