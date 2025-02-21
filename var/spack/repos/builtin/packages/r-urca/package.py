# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUrca(RPackage):
    """Unit Root and Cointegration Tests for Time Series Data.

    Unit root and cointegration tests encountered in applied econometric
    analysis are implemented."""

    cran = "urca"

    license("GPL-2.0-or-later")

    version("1.3-4", sha256="fe3d6ce5041f1e7caaf3137dfb6187640bcd2d208e19c59ee1202355ac0acb16")
    version("1.3-3", sha256="43baa8b6735f8325a69e6a43686f4fecd77a0eb7f60da25b4fc5c51b9271e9f1")
    version("1.3-0", sha256="621cc82398e25b58b4a16edf000ed0a1484d9a0bc458f734e97b6f371cc76aaa")

    depends_on("r@2.0.0:", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))
