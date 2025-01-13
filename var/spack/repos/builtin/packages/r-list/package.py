# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RList(RPackage):
    """Allows researchers to conduct multivariate statistical analyses
    of survey data with list experiments."""

    homepage = "https://cran.r-project.org/web/packages/list/index.html"
    cran = "list"

    license("GPL-2.0-or-later", checked_by="wdconinc")

    version("9.2.6", sha256="6a2b1dd9cdee87d739605fb38463cb6e04680c94b73f51fbd39b5552a62432e4")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-sandwich@2.3-3:", type=("build", "run"))
    depends_on("r-vgam@0.9-8:", type=("build", "run"))
    depends_on("r-magic@1.5-6:", type=("build", "run"))
    depends_on("r-gamlss-dist@4.3-4:", type=("build", "run"))
    depends_on("r-mass@7.3-40:", type=("build", "run"))
    depends_on("r-quadprog@1.5-5:", type=("build", "run"))
    depends_on("r-corpcor@1.6.7:", type=("build", "run"))
    depends_on("r-mvtnorm@1.0-2:", type=("build", "run"))
    depends_on("r-coda@0.17-1:", type=("build", "run"))
    depends_on("r-arm", type=("build", "run"))
