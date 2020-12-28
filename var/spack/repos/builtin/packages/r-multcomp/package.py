# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMultcomp(RPackage):
    """Simultaneous tests and confidence intervals for general linear
    hypotheses in parametric models, including linear, generalized linear,
    linear mixed effects, and survival models. The package includes demos
    reproducing analyzes presented in the book "Multiple Comparisons Using R"
    (Bretz, Hothorn, Westfall, 2010, CRC Press)."""

    homepage = "http://multcomp.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/multcomp_1.4-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/multcomp"

    version('1.4-10', sha256='29bcc635c0262e304551b139cd9ee655ab25a908d9693e1cacabfc2a936df5cf')
    version('1.4-8', sha256='a20876619312310e9523d67e9090af501383ce49dc6113c6b4ca30f9c943a73a')
    version('1.4-6', sha256='fe9efbe671416a49819cbdb9137cc218faebcd76e0f170fd1c8d3c84c42eeda2')

    depends_on('r-mvtnorm@1.0-10:', type=('build', 'run'))
    depends_on('r-survival@2.39-4:', type=('build', 'run'))
    depends_on('r-th-data@1.0-2:', type=('build', 'run'))
    depends_on('r-sandwich@2.3-0:', type=('build', 'run'))
    depends_on('r-codetools', type=('build', 'run'))
