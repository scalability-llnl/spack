# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocstyle(RPackage):
    """Standard styles for vignettes and other Bioconductor documents.

    Provides standard formatting styles for Bioconductor PDF and HTML
    documents. Package vignettes illustrate use and functionality."""

    bioc = "BiocStyle"

    version("2.34.0", commit="0a042423c1f4e8bc6dece3c31fcc5e9750a2f9ab")
    version("2.32.1", commit="bd5e8295d5a1891189553c1f5b0177ea90001366")
    version("2.30.0", commit="48deba5c4d84ea9d236256a673a58ab3f1d6c2cf")
    version("2.28.0", commit="b358aa5d3f9c68629e9abf50ffceccbf77226ea8")
    version("2.26.0", commit="add035498bdce76d71a0afa22a063c2d8e5588bc")
    version("2.24.0", commit="53095b534b7e6c80a33a67b5f2db0db8f00db902")
    version("2.22.0", commit="86250b637afa3a3463fac939b99c0402b47876ea")
    version("2.18.1", commit="956f0654e8e18882ba09305742401128c9c7d47d")
    version("2.12.0", commit="0fba3fe6e6a38504f9aadcd3dc95bb83d7e92498")
    version("2.10.0", commit="8fc946044c6b6a8a3104ddbc546baed49ee3aa70")
    version("2.8.2", commit="3210c19ec1e5e0ed8d5a2d31da990aa47b42dbd8")
    version("2.6.1", commit="5ff52cbb439a45575d0f58c4f7a83195a8b7337b")
    version("2.4.1", commit="ef10764b68ac23a3a7a8ec3b6a6436187309c138")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-bookdown", type=("build", "run"))
    depends_on("r-knitr@1.12:", type=("build", "run"))
    depends_on("r-knitr@1.30:", type=("build", "run"), when="@2.18.1:")
    depends_on("r-rmarkdown@1.2:", type=("build", "run"))
    depends_on("r-yaml", type=("build", "run"))
    depends_on("r-biocmanager", type=("build", "run"), when="@2.10.0:")
