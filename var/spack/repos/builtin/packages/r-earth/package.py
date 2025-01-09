# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REarth(RPackage):
    """Multivariate Adaptive Regression Splines.

    Build regression models using the techniques in Friedman's papers
    "Fast MARS" and "Multivariate Adaptive Regression Splines"
    <doi:10.1214/aos/1176347963>."""

    cran = "earth"

    license("GPL-3.0-only")

    version("5.3.3", sha256="786a0fcabb3db13e0e0a4ba61ecccb7e171030b39bc97926f8e7159485d2f572")
    version("5.3.2", sha256="c844d75edf9a2706a911bb05ed4287aad9acf6f3fed357e037763a300eac0bea")
    version("5.3.1", sha256="0bbe06ba974ceb8ec5de1d59cb53f9487d1828d7130fe2503c48b6cb449c4b03")
    version("5.3.0", sha256="05ace806271a74b3ddf8718a93237fe2a8550a8659ebd87f8079c0bda5e02437")
    version("5.1.2", sha256="326f98e8c29365ca3cd5584cf2bd6529358f5ef81664cbd494162f92b6c3488d")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-formula@1.2-3:", type=("build", "run"))
    depends_on("r-plotmo@3.5.4:", type=("build", "run"))
    depends_on("r-plotmo@3.6.0:", type=("build", "run"), when="@5.3.0")
    depends_on("r-plotmo@3.6.0:", type=("build", "run"), when="@5.3.3:")

    depends_on("r-teachingdemos@2.10:", type=("build", "run"), when="@:5.3.2")
