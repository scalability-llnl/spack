# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHydrogof(RPackage):
    """Goodness-of-Fit Functions for Comparison of Simulated and Observed
    Hydrological Time Series.

    S3 functions implementing both statistical and graphical goodness-of-fit
    measures between observed and simulated values, mainly oriented to be used
    during the calibration, validation, and application of hydrological models.
    Missing values in observed and/or simulated values can be removed before
    computations. Comments / questions / collaboration of any kind are very
    welcomed."""

    cran = "hydroGOF"

    version("0.6-0", sha256="fb1839da5d6c2d0bbff961b4bb39d149b487b59dc36017aada9d3484a842269e")
    version("0.4-0", sha256="6a109740e36549a9369b5960b869e5e0a296261df7b6faba6cb3bd338d59883b")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-zoo@1.7-2:", type=("build", "run"))
    depends_on("r-hydrotsm@0.5-0:", type=("build", "run"))
    depends_on("r-xts@0.8-2:", type=("build", "run"))
