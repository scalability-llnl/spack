# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatUnivar(RPackage):
    """Estimation of one-dimensional probability distributions including
    kernel density estimation, weighted empirical cumulative distribution
    functions, Kaplan-Meier and reduced-sample estimators for right-censored
    data, heat kernels, kernel properties, quantiles and integration."""

    homepage = "http://spatstat.org/"
    cran = "spatstat.univar"

    license("GPL-2.0-or-later", checked_by="wdconinc")

    version("3.0-0", sha256="00bc501d9bec32231207f0562433193bd680606ce465131caa5e2704b4ff4771")

    depends_on("r@3.5.0:", type=("build", "run"), when="@3.0-0:")
    depends_on("r-spatstat-utils@3.0-5:", type=("build", "run"), when="@2.0-3.011:")
