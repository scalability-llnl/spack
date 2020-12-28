# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFitdistrplus(RPackage):
    """Extends the fitdistr() function (of the MASS package) with several
    functions to help the fit of a parametric distribution to non-censored or
    censored data. Censored data may contain left censored, right censored and
    interval censored values, with several lower and upper bounds. In addition
    to maximum likelihood estimation (MLE), the package provides moment
    matching (MME), quantile matching (QME) and maximum goodness-of-fit
    estimation (MGE) methods (available only for non-censored data). Weighted
    versions of MLE, MME and QME are available. See e.g. Casella & Berger
    (2002). Statistical inference. Pacific Grove."""

    homepage = "https://lbbe.univ-lyon1.fr/fitdistrplus.html"
    url      = "https://cloud.r-project.org/src/contrib/fitdistrplus_1.0-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fitdistrplus"

    version('1.0-14', sha256='85082590f62aa08d99048ea3414c5cc1e5b780d97b3779d2397c6cb435470083')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-npsurv', type=('build', 'run'))
