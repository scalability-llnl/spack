# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDosnow(RPackage):
    """Provides a parallel backend for the %dopar% function using the snow
    package of Tierney, Rossini, Li, and Sevcikova."""

    homepage = "https://cloud.r-project.org/package=doSNOW"
    url      = "https://cloud.r-project.org/src/contrib/doSNOW_1.0.18.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/doSNOW"

    version('1.0.18', sha256='70e7bd82186e477e3d1610676d4c6a75258ac08f104ecf0dcc971550ca174766')

    depends_on('r@2.5.0:', type=('build', 'run'))
    depends_on('r-foreach@1.2.0:', type=('build', 'run'))
    depends_on('r-iterators@1.0.0:', type=('build', 'run'))
    depends_on('r-snow@0.3.0:', type=('build', 'run'))
