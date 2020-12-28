# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUrltools(RPackage):
    """urltools: Vectorised Tools for URL Handling and Parsing"""

    homepage = "https://github.com/Ironholds/urltools/"
    url      = "https://cloud.r-project.org/src/contrib/urltools_1.7.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/urltools"

    version('1.7.3', sha256='6020355c1b16a9e3956674e5dea9ac5c035c8eb3eb6bbdd841a2b5528cafa313')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-triebeard', type=('build', 'run'))
