# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUrlchecker(RPackage):
    """Run CRAN URL Checks from Older R Versions.

    Provide the URL checking tools available in R 4.1+ as a package for earlier
    versions of R. Also uses concurrent requests so can be much faster than the
    serial versions."""

    cran = "urlchecker"

    license("GPL-3.0-only")

    version("1.0.1", sha256="62165ddbe1b748b58c71a50c8f07fdde6f3d19a7b39787b9fa2b4f9216250318")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r-cli", type=("build", "run"))
    depends_on("r-curl", type=("build", "run"))
    depends_on("r-xml2", type=("build", "run"))
