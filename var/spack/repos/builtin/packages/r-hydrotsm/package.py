# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHydrotsm(RPackage):
    """Time Series Management, Analysis and Interpolation for Hydrological
    Modelling.

    S3 functions for management, analysis, interpolation and plotting of time
    series used in hydrology and related environmental sciences. In particular,
    this package is highly oriented to hydrological modelling tasks. The focus
    of this package has been put in providing a collection of tools useful for
    the daily work of hydrologists (although an effort was made to optimise
    each function as much as possible, functionality has had priority over
    speed). Bugs / comments / questions / collaboration of any kind are very
    welcomed, and in particular, datasets that can be included in this package
    for academic purposes."""

    cran = "hydroTSM"

    version("0.7-0", sha256="a6e1f0f74a5b8f3a7c05d020739342278b0a54e7b63a66a755db5599ebf94a8e")
    version("0.6-0", sha256="5be759845ce05ca579ed2657c85d497b78c3060d737e84fcd457153045db4ad7")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.7-0:")
    depends_on("r-zoo@1.7-2:", type=("build", "run"))
    depends_on("r-xts@0.9-7:", type=("build", "run"))
    depends_on("r-e1071", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-classint", type=("build", "run"), when="@0.7-0:")

    depends_on("r-gstat", type=("build", "run"), when="@:0.6.0")
    depends_on("r-automap", type=("build", "run"), when="@:0.6.0")
    depends_on("r-sp@1.1-0:", type=("build", "run"), when="@:0.6.0")
    depends_on("r-maptools", type=("build", "run"), when="@:0.6.0")
