# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RExomedepth(RPackage):
    """Calls Copy Number Variants from Targeted Sequence Data.

    Calls copy number variants (CNVs) from targeted sequence data, typically
    exome sequencing experiments designed to identify the genetic basis of
    Mendelian disorders."""

    cran = "ExomeDepth"

    version("1.1.16", sha256="7ba6b51e7ea435a2799b25d99bb9f48e2b1e99e15e47f88e514e98120b4cebe4")
    version("1.1.15", sha256="112bcb536f5766d9d0b55e064feedd6727ccab14cb1edfdba1f0d7b890e55ad2")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-rsamtools", type=("build", "run"))
    depends_on("r-genomicranges@1.23.0:", type=("build", "run"))
    depends_on("r-aod", type=("build", "run"))
    depends_on("r-vgam@0.8.4:", type=("build", "run"))
    depends_on("r-genomicalignments", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
