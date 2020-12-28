# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPmcmr(RPackage):
    """The Kruskal and Wallis one-way analysis of variance by ranks or van
       der Waerden's normal score test can be employed, if the data do not
       meet the assumptions for one-way ANOVA. Provided that significant
       differences were detected by the omnibus test, one may be interested
       in applying post-hoc tests for pairwise multiple comparisons (such as
       Nemenyi's test, Dunn's test, Conover's test, van der Waerden's test).
       Similarly, one-way ANOVA with repeated measures that is also referred
       to as ANOVA with unreplicated block design can also be conducted via
       the Friedman-Test or the Quade-test. The consequent post-hoc pairwise
       multiple comparison tests according to Nemenyi, Conover and Quade are
       also provided in this package. Finally Durbin's test for a two-way
       balanced incomplete block design (BIBD) is also given in this
       package."""

    homepage = "https://cloud.r-project.org/package=PMCMR"
    url      = "https://cloud.r-project.org/src/contrib/PMCMR_4.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/PMCMR"

    version('4.3', sha256='328a2880dd614dc412e8dca21d29ed9d5eea29ccbe0eff98c8068100856c7b25')
    version('4.1', sha256='6c164e2976c59ddd27297433a34fa61b1e70b9e26265abdf9c8af1b639d2d555')

    depends_on('r@3.0.0:', type=('build', 'run'))
