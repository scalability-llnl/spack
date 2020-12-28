# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROrdinal(RPackage):
    """Implementation of cumulative link (mixed) models also known as ordered
    regression models, proportional odds models, proportional hazards models
    for grouped survival times and ordered logit/probit/... models. Estimation
    is via maximum likelihood and mixed models are fitted with the Laplace
    approximation and adaptive Gauss-Hermite quadrature. Multiple random effect
    terms are allowed and they may be nested, crossed or partially
    nested/crossed. Restrictions of symmetry and equidistance can be imposed on
    the thresholds (cut-points/intercepts). Standard model methods are
    available (summary, anova, drop-methods, step, confint, predict etc.) in
    addition to profile methods and slice methods for visualizing the
    likelihood function and checking convergence."""

    homepage = "https://github.com/runehaubo/ordinal"
    url      = "https://cloud.r-project.org/src/contrib/ordinal_2019.4-25.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ordinal"

    version('2019.4-25', sha256='2812ad7a123cae5dbe053d1fe5f2d9935afc799314077eac185c844e3c9d79df')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('r-ucminf', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
