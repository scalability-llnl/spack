# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRstantools(RPackage):
    """Tools for Developing R Packages Interfacing with 'Stan'

    Provides various tools for developers of R packages interfacing with 'Stan'
    <https://mc-stan.org>, including functions to set up the required  package
    structure, S3 generics and default methods to unify function naming  across
    'Stan'-based R packages, and vignettes with recommendations for
    developers."""

    homepage = "http://discourse.mc-stan.org/"
    url      = "https://cloud.r-project.org/src/contrib/rstantools_1.5.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rstantools"

    version('2.1.1', sha256='c95b15de8ec577eeb24bb5206e7b685d882f88b5e6902efda924b7217f463d2d')
    version('1.5.1', sha256='5cab16c132c12e84bd08e18cd6ef25ba39d67a04ce61015fc4490659c7cfb485')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r-desc', when='@2.1.1:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.16:', when='@2.1.1:', type=('build', 'run'))
    depends_on('r-rcppparallel@5.0.1:', when='@2.1.1:', type=('build', 'run'))
    depends_on('pandoc', type='build')
