# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRoc(RPackage):
    """utilities for ROC, with microarray focus.

    Provide utilities for ROC, with microarray focus."""

    bioc = "ROC"

    version("1.76.0", commit="905ee01be734ed0a5674a4ce2cdc0cdea9d01cb9")
    version("1.74.0", commit="982ad4d3606b19b8460e8a8af7cfe7c30b83f9b9")
    version("1.72.0", commit="c5d083b01314280dd43eb4cddd8a7fde8b5dce18")
    version("1.70.0", commit="44fd639958b9b1be4f8f731dc2be9dd91b2fa632")
    version("1.66.0", commit="62701ee41f48f99d15344127384fa032db69486f")
    version("1.62.0", commit="60250fdb091f6a938709b8a2cffe6442ee22a9a2")

    depends_on("cxx", type="build")  # generated

    depends_on("r@1.9.0:", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"))
