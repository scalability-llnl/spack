# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCopula(RPackage):
    """Multivariate Dependence with Copulas.

    Classes (S4) of commonly used elliptical, Archimedean, extreme-value and
    other copula families, as well as their rotations, mixtures and
    asymmetrizations. Nested Archimedean copulas, related tools and special
    functions. Methods for density, distribution, random number generation,
    bivariate dependence measures, Rosenblatt transform, Kendall distribution
    function, perspective and contour plots. Fitting of copula models with
    potentially partly fixed parameters, including standard errors. Serial
    independence tests, copula specification tests (independence,
    exchangeability, radial symmetry, extreme-value dependence,
    goodness-of-fit) and model selection based on cross-validation. Empirical
    copula, smoothed versions, and non-parametric estimators of the Pickands
    dependence function."""

    cran = "copula"

    license("GPL-3.0-or-later OR custom")

    version("1.1-4", sha256="f4d78b7f4860797620dfe15c62cbeeb319b2dbbacab75062652d467c4ef6504f")
    version("1.1-2", sha256="88f9454d25e4dcdf53d8ca5156daf48e664769f5e13b1e835ed64f37251587d3")
    version("1.1-0", sha256="9ab76e6256534db2a18d3880143b8c67e385767010de861bbde25212aa75d924")
    version("1.0-1", sha256="d09b2ccffc7379e48b00952aa6b282baf502feebaf55cc44e93f881d7b909742")
    version("0.999-20", sha256="7d3d47bce2dacb05b94a772f84dbf3d83c99ac2ac11e5f1b4b03d50d9d5c0fb0")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.0-1:")
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-matrix@1.5-0:", type=("build", "run"), when="@1.1-2:")
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-colorspace", type=("build", "run"))
    depends_on("r-gsl", type=("build", "run"))
    depends_on("r-adgoftest", type=("build", "run"))
    depends_on("r-stabledist@0.6-4:", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))
    depends_on("r-pcapp", type=("build", "run"))
    depends_on("r-pspline", type=("build", "run"))
    depends_on("r-numderiv", type=("build", "run"))
