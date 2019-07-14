# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDorng(RPackage):
    """Provides functions to perform reproducible parallel foreach loops,
       using independent random streams as generated by L'Ecuyer's combined
       multiple-recursive generator
       [L'Ecuyer (1999), <doi:10.1287/opre.47.1.159>]. It enables to easily
       convert standard %dopar% loops into fully reproducible loops,
       independently of the number of workers, the task scheduling strategy,
       or the chosen parallel environment and associated foreach backend."""

    homepage = "https://cran.rstudio.com/web/packages/doRNG/index.html"
    url      = "https://cran.rstudio.com/src/contrib/doRNG_1.6.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/doRNG"

    version('1.7.1', sha256='27533d54464889d1c21301594137fc0f536574e3a413d61d7df9463ab12a67e9')
    version('1.6.6', 'ffb26024c58c8c99229470293fbf35cf')

    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-rngtools', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
    depends_on('r-pkgmaker', type=('build', 'run'))
