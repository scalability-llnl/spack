# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCopula(RPackage):
    """Classes (S4) of commonly used elliptical, Archimedean, extreme-value and
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

    homepage = "http://copula.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/copula_0.999-20.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/copula"

    version('0.999-20', sha256='7d3d47bce2dacb05b94a772f84dbf3d83c99ac2ac11e5f1b4b03d50d9d5c0fb0')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-gsl', type=('build', 'run'))
    depends_on('r-adgoftest', type=('build', 'run'))
    depends_on('r-stabledist@0.6-4:', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-pcapp', type=('build', 'run'))
    depends_on('r-pspline', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
