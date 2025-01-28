# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPlotmo(RPackage):
    """Plot a Model's Residuals, Response, and Partial Dependence Plots.

    Plot model surfaces for a wide variety of models using partial dependence
    plots and other techniques. Also plot model residuals and other information
    on the model."""

    cran = "plotmo"

    license("GPL-3.0-only")

    version("3.6.3", sha256="6917cd8185325f1f2998fb14def9e6a8d93f1b708cf70d7c443d3960c9189b7b")
    version("3.6.2", sha256="cde33a8ec558b12d8e11d7d0531e73f6678a25ee589b79897d2fc425a3fd353c")
    version("3.6.1", sha256="245a0c87f0cca08746c6fdc60da2e3856cd69b1a2b7b5641293c620d4ae04343")
    version("3.6.0", sha256="c05afcc442f9542868beea5c3c40fb93b049f9b61c42725b2a1e2bc750c241e3")
    version("3.5.6", sha256="78f08dc897136d21fa8ade2acb6290351b569d29eb0592c7074c0be3cf2aa594")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-formula@1.2-3:", type=("build", "run"))
    depends_on("r-plotrix", type=("build", "run"))

    depends_on("r-teachingdemos", type=("build", "run"), when="@:3.6.2")
