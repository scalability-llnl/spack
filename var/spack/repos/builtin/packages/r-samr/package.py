# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSamr(RPackage):
    """SAM: Significance Analysis of Microarrays.

    Significance Analysis of Microarrays for differential expression analysis,
    RNAseq data and related problems."""

    cran = "samr"

    license("LGPL-2.0-or-later")

    version("3.0", sha256="25f88ac002c2adce8881a562241bc12d683810a05defb553e8e3d4878f037506")
    version("2.0", sha256="090b5becd91d60f4bb8269df5c9bc19a03c09917d327b28e75b0ee7b80624e67")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r-impute", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-shiny", type=("build", "run"), when="@3.0:")
    depends_on("r-shinyfiles", type=("build", "run"), when="@3.0:")
    depends_on("r-openxlsx", type=("build", "run"), when="@3.0:")
    depends_on("r-gsa", type=("build", "run"), when="@3.0:")
