# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSfsmisc(RPackage):
    """Utilities from 'Seminar fuer Statistik' ETH Zurich

    Useful utilities ['goodies'] from Seminar fuer Statistik ETH Zurich, some
    of which were ported from S-plus in the 1990s.; For graphics, have pretty
    (Log-scale) axes, an enhanced Tukey-Anscombe plot, combining histogram and
    boxplot, 2d-residual plots, a 'tachoPlot()', pretty arrows, etc.; For
    robustness, have a robust F test and robust range().; For system support,
    notably on Linux, provides 'Sys.*()' functions with more access to system
    and CPU information.; Finally, miscellaneous utilities such as simple
    efficient prime numbers, integer codes, Duplicated(), toLatex.numeric() and
    is.whole()."""

    homepage = "https://cloud.r-project.org/package=sfsmisc"
    url      = "https://cloud.r-project.org/src/contrib/sfsmisc_1.1-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sfsmisc"

    version('1.1-8', sha256='b6556af5f807f0769489657a676422cb0734f3d6c918543d2989ef17febc1fa5')
    version('1.1-4', sha256='44b6a9c859922e86b7182e54eb781d3264f3819f310343518ebc66f54f305c7d')
    version('1.1-3', sha256='58eff7d4a9c79212321858efe98d2a6153630e263ff0218a31d5e104b8b545f8')
    version('1.1-0', sha256='7f430cf3ebb95bac806fbf093fb1e2112deba47416a93be8d5d1064b76bc0015')

    depends_on('r@3.0.1:', when='@:1.1-1', type=('build', 'run'))
    depends_on('r@3.2.0:', when='@1.1-2:', type=('build', 'run'))
