# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGamlss(RPackage):
    """Generalised Additive Models for Location Scale and Shape.

    Functions for fitting the Generalized Additive Models for Location Scale
    and Shape introduced by Rigby and Stasinopoulos (2005),
    <doi:10.1111/j.1467-9876.2005.00510.x>. The models use a distributional
    regression approach where all the parameters of the conditional
    distribution of the response variable are modelled using explanatory
    variables."""

    cran = "gamlss"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("5.4-22", sha256="01e6908df92691147b884a8d58025473e18d7bf58d5f5a2d7e4f18b2a451fe2d")
    version("5.4-12", sha256="9f791039f7e5c3cf3f6a2da955994a8c41c43044a2d77d99b289e4f82118a6f0")
    version("5.4-3", sha256="6619d4fdc183ab492615d44961a126c827d18db20a0d59362e54de877f0a3076")
    version("5.3-4", sha256="72707187471fd35c5379ae8c9b7b0ca87e302557f09cb3979d1cdb2e2500b01a")
    version("5.2-0", sha256="d3927547109064cbe7b0f955144f53204b5dc86c6b2dbc8f0551a74140ab02e1")
    version("5.1-4", sha256="e2fc36fe6ca3a69d69cdafd9533a4ff35090fdfb01df126f6a49156f4aa3376c")
    version("5.1-3", sha256="d37d121bc2acdbacc20cea04a1ed4489a575079e2a7b17b4a9823ee283857317")
    version("5.1-2", sha256="0d404e74768a8f98c6a5e9a48bd2cf4280125831a5dcd8c7f7b57922f57e016b")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-gamlss-data@5.0-0:", type=("build", "run"))
    depends_on("r-gamlss-dist@4.3.1:", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
