# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSurvey(RPackage):
    """Summary statistics, two-sample tests, rank tests, generalised linear
    models, cumulative link models, Cox models, loglinear models, and general
    maximum pseudolikelihood estimation for multistage stratified,
    cluster-sampled, unequally weighted survey samples. Variances by Taylor
    series linearisation or replicate weights. Post-stratification,
    calibration, and raking. Two-phase subsampling designs. Graphics. PPS
    sampling without replacement. Principal components, factor analysis."""

    homepage = "http://r-survey.r-forge.r-project.org/survey/"
    url      = "https://cloud.r-project.org/src/contrib/survey_3.30-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/survey"

    version('3.36', sha256='90f32e9d2b52eacf881e6717a4b5edfc5a3beb5da516f8372293549589d79475')
    version('3.35-1', sha256='11e5ddde9c8c21dfaed0b1247036e068ad32782c76ff71f7937eb7585dd364db')
    version('3.30-3', sha256='be45d00b22d857e66905789031f2db1037505f80ce15d4b0ea84dabb03bc9e6d')

    depends_on('r@2.14.0:', when='@:3.31-5', type=('build', 'run'))
    depends_on('r@2.16.0:', when='@3.32:3.34', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@3.35:', type=('build', 'run'))
    depends_on('r-matrix', when='@3.31:', type=('build', 'run'))
    depends_on('r-survival', when='@3.31:', type=('build', 'run'))
    depends_on('r-lattice', when='@3.31:', type=('build', 'run'))
    depends_on('r-minqa', when='@3.34:', type=('build', 'run'))
    depends_on('r-numderiv', when='@3.34:', type=('build', 'run'))
    depends_on('r-mitools@2.4:', when='@3.36:', type=('build', 'run'))
