# Copyright Spack Project Developers. See COPYRIGHT file for details.
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

    version("1.18.0", commit="31887d4d482a1d604fbcad15020fc30d441a66b4")
    version("1.16.0", commit="0a27ae63be9d7fa486f55992332f84b4259c97af")
    version("1.14.3", commit="6412875836db012cd9c490539a82b9887afd6389")
    version("1.12.0", commit="26c1c354526eb8d806268427a7c40b31bb89f489")

    depends_on("r-reticulate", type=("build", "run"))
    depends_on("r-dir-expiry", type=("build", "run"))
    depends_on("r-basilisk-utils", type=("build", "run"))
    depends_on("r-basilisk-utils@1.15.1:", type=("build", "run"), when="@1.15.1:")
