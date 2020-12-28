# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSmoof(RPackage):
    """Provides generators for a high number of both single- and
       multi- objective test functions which are frequently used for the
       benchmarking of (numerical) optimization algorithms. Moreover, it offers
       a set of convenient functions to generate, plot and work with objective
       functions."""

    homepage = "http://github.com/jakobbossek/smoof"
    url      = "https://cloud.r-project.org/src/contrib/smoof_1.5.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/smoof"

    version('1.5.1', sha256='cfb6f6460e9593351428656b225b5ba3867a216d35a05f2babdb20db6ba35306')
    version('1.5', sha256='9b73ad5bfc8e1120c9651539ea52b1468f316cc7fc5fef8afd6d357adf01504c')

    depends_on('r-paramhelpers@1.8:', type=('build', 'run'))
    depends_on('r-bbmisc@1.6:', type=('build', 'run'))
    depends_on('r-checkmate@1.1:', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.1:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-plot3d', type=('build', 'run'))
    depends_on('r-plotly', type=('build', 'run'))
    depends_on('r-mco', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-rjsonio', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
