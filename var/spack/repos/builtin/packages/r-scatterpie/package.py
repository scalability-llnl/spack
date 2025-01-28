# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScatterpie(RPackage):
    """Scatter Pie Plot.

    Creates scatterpie plots, especially useful for plotting pies on a map."""

    cran = "scatterpie"

    license("Artistic-2.0")

    version("0.2.3", sha256="704f1072ff934729aefdd659e5c81e62b59f5ae94dc36a1e1f52085dce896447")
    version("0.1.9", sha256="517fd6cc297aa33f0fbb2643e35ca41dc971166ea2e8ed78460bd4ef7a77a687")
    version("0.1.8", sha256="a6ccc63a8be63fa113704cf5d4893c1ec1b75d3081ab971bd70e650e708872a0")
    version("0.1.7", sha256="3f7807519cfe135066ca79c8d8a09b59da9aa6d8aaee5e9aff40cca3d0bebade")
    version("0.1.5", sha256="e13237b7effc302acafc1c9b520b4904e55875f4a3b804f653eed2940ca08840")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r@4.1.0:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-ggforce", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-ggfun", type=("build", "run"), when="@0.1.7:")
    depends_on("r-tidyr", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"), when="@0.1.9:")

    depends_on("r-rvcheck", type=("build", "run"), when="@:0.1.5")
