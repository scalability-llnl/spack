# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLavaan(RPackage):
    """Latent Variable Analysis.

    Fit a variety of latent variable models, including confirmatory factor
    analysis, structural equation modeling and latent growth curve models."""

    cran = "lavaan"

    license("GPL-2.0-or-later")

    version("0.6-18", sha256="b907cacd6c4a2320138cb2206f17b60acf077453540bcb9cc94659fc9a48df51")
    version("0.6-15", sha256="9a43f3e999f9b3003a8c46a615902e01d6701d28a871d657751dd2ff3928ed9b")
    version("0.6-12", sha256="8048273e4102f8355ba123c8aff94a9e5a8e9ac9e02a73e986b106ceed4d079e")
    version("0.6-11", sha256="2cc193b82463a865cd8dadb7332409fdebf47e4035d5fe8dbf3414a7ae18d308")
    version("0.6-10", sha256="4d6944eb6d5743e7a2a2c7b56aec5d5de78585a52789be235839fb9f5f468c37")
    version("0.6-9", sha256="d404c4eb40686534f9c05f24f908cd954041f66d1072caea4a3adfa83a5f108a")
    version("0.6-8", sha256="40e204909100b7338619ae23cd87e0a4058e581c286da2327f36dbb3834b84a2")

    depends_on("r@3.4:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-mnormt", type=("build", "run"))
    depends_on("r-pbivnorm", type=("build", "run"))
    depends_on("r-numderiv", type=("build", "run"))
    depends_on("r-quadprog", type=("build", "run"), when="@0.6-15:")
