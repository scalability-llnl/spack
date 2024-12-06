# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBasilisk(RPackage):
    """Freezing Python Dependencies Inside Bioconductor Packages.

    Installs a self-contained conda instance that is managed by the
    R/Bioconductor installation machinery. This aims to provide a consistent
    Python environment that can be used reliably by Bioconductor packages.
    Functions are also provided to enable smooth interoperability of multiple
    Python environments in a single R session."""

    bioc = "basilisk"

    license("GPL-3.0-or-later")

    version("1.12.0", commit="26c1c354526eb8d806268427a7c40b31bb89f489")

    depends_on("r-reticulate", type=("build", "run"))
    depends_on("r-dir-expiry", type=("build", "run"))
    depends_on("r-basilisk-utils", type=("build", "run"))
