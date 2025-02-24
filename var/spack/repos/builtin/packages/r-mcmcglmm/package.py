# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMcmcglmm(RPackage):
    """MCMC Generalised Linear Mixed Models.

    Fits Multivariate Generalised Linear Mixed Models (and related models)
    using Markov chain Monte Carlo techniques (Hadfield 2010 J. Stat.
    Soft.)."""

    cran = "MCMCglmm"

    version("2.36", sha256="66ffd9aaf8035c7abe7208c8514c60cb56c8c6a170de207d6608f5c44a4f8af1")
    version("2.34", sha256="829151cca93b05979ece98157e7789d5e5c1c0b4942d69aa9886de03d16091f1")
    version("2.33", sha256="b56d72e799f8ed5fa2a05ecc743e5b8051f9cc2de57ad3e6de2dcb1c1715d4fc")
    version("2.32", sha256="a9156e1e0d0f912f2f239476dc8765dc61c480f903381be7ec5db05bd6d3f0b3")
    version("2.30", sha256="714250fe6ebdd1bd3dc284f7fcb92326de1273b0c34d31e71dc825312527e042")
    version("2.29", sha256="13ba7837ea2049e892c04e7ec5c83d5b599a7e4820b9d875f55ec40fc2cc67b4")
    version("2.28", sha256="7d92e6d35638e5e060a590b92c3b1bfc02a11386276a8ab99bceec5d797bfc2a")
    version("2.25", sha256="3072316bf5c66f6db5447cb488395ff019f6c47122813467384474f340643133")

    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-coda", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-corpcor", type=("build", "run"))
    depends_on("r-tensora", type=("build", "run"))
    depends_on("r-cubature", type=("build", "run"))
