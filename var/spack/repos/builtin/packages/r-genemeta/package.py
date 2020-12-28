# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenemeta(RPackage):
    """MetaAnalysis for High Throughput Experiments.

       A collection of meta-analysis tools for analysing high throughput
       experimental data"""

    homepage = "https://bioconductor.org/packages/GeneMeta"
    git      = "https://git.bioconductor.org/packages/GeneMeta.git"

    version('1.56.0', commit='cb2c9e353d34ea9f3db06cb236c7a89674f2682d')
    version('1.54.0', commit='932553cd8df82b7df804fccda9bfd4b0f36d79d7')
    version('1.52.0', commit='1f21759984a5852c42a19e89ee53ffd72053d49c')
    version('1.50.0', commit='0f8603653285698ed451fcbf536a4b3f90015f92')
    version('1.48.0', commit='68c65304d37f5a4722cf4c25afb23214c3a2f4c8')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-biobase@2.5.5:', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
