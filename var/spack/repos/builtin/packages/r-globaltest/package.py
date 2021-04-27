# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGlobaltest(RPackage):
    """Testing Groups of Covariates/Features for Association with a Response
    Variable, with Applications to Gene Set Testing:

    The global test tests groups of covariates (or features) for association
    with a response variable. This package implements the test with diagnostic
    plots and multiple testing utilities, along with several functions to
    facilitate the use of this test for gene set testing of GO and KEGG
    terms."""

    bioc     = "globaltest"

    version('5.44.0', commit='571933d5c779a241740be913ff49ecdd59bcbc45')

    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
