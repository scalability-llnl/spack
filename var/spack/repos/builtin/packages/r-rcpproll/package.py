# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcpproll(RPackage):
    """Efficient Rolling / Windowed Operations.

    Provides fast and efficient routines for common rolling / windowed
    operations. Routines for the efficient computation of windowed mean,
    median, sum, product, minimum, maximum, standard deviation and variance are
    provided."""

    cran = "RcppRoll"

    version("0.3.1", sha256="d2f5d978b6feb8510ec1a1a50ba0e8bf9002bb77bfad7d120f5b30b8f56036df")
    version("0.3.0", sha256="cbff2096443a8a38a6f1dabf8c90b9e14a43d2196b412b5bfe5390393f743f6b")

    depends_on("r@2.15.1:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
