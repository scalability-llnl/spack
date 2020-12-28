# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDismo(RPackage):
    """Functions for species distribution modeling, that is, predicting
       entire geographic distributions form occurrences at a number of sites
       and the environment at these sites."""

    homepage = "https://cloud.r-project.org/package=dismo"
    url      = "https://cloud.r-project.org/src/contrib/dismo_1.1-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/dismo"

    version('1.1-4', sha256='f2110f716cd9e4cca5fd2b22130c6954658aaf61361d2fe688ba22bbfdfa97c8')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-raster@2.5-2:', type=('build', 'run'))
    depends_on('r-sp@1.2-0:', type=('build', 'run'))
