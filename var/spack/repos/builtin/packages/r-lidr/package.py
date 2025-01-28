# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLidr(RPackage):
    """Airborne LiDAR data manipulation and visualisation for forestry application"""

    homepage = "https://github.com/r-lidar/lidR"
    url = "https://cran.r-project.org/src/contrib/lidR_4.1.2.tar.gz"

    maintainers("sidpbury")

    license("GPL-3.0")

    version("4.1.2", sha256="e452c35c189fb8bcfedb53b2cb1184a6feee11c2f3ccf1db4b161a9ce700a9eb")

    variant("suggests", default=False, description="adding suggests helps masking issues")

    # Depends
    depends_on("r@3.5.0:", type=("build", "run"))

    # Imports
    depends_on("r-classint", type=("build", "run"))
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-lazyeval", type=("build", "run"))
    depends_on("r-rcpp@1.0.3:", type=("build", "run"))
    depends_on("r-rgl", type=("build", "run"))
    depends_on("r-rlas@1.5.0:", type=("build", "run"))
    depends_on("r-sf", type=("build", "run"))
    depends_on("r-stars", type=("build", "run"))
    depends_on("r-terra@1.5:", type=("build", "run"))

    # Linking To
    depends_on("r-bh", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))

    # Suggests
    depends_on("r-future", type=("build", "run"), when="+suggests")
    depends_on("r-geometry", type=("build", "run"), when="+suggests")
    depends_on("r-gstat", type=("build", "run"), when="+suggests")
    depends_on("r-raster", type=("build", "run"), when="+suggests")
    depends_on("r-rjson", type=("build", "run"), when="+suggests")
    depends_on("r-mapview", type=("build", "run"), when="+suggests")
    depends_on("r-progress", type=("build", "run"), when="+suggests")
    depends_on("r-sp", type=("build", "run"), when="+suggests")
    depends_on("r-testthat@2.1.0:", type=("build", "run"), when="+suggests")
    depends_on("r-knitr", type=("build", "run"), when="+suggests")
    depends_on("r-rmarkdown", type=("build", "run"), when="+suggests")
