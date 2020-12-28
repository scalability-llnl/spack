# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REuropepmc(RPackage):
    """europepmc: R Interface to the Europe PubMed Central RESTful Web
       Service"""

    homepage = "http://github.com/ropensci/europepmc/"
    url      = "https://cloud.r-project.org/src/contrib/europepmc_0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/europepmc"

    version('0.3', sha256='5044a253d223e2bb8502063cd03c0fe4db856467e497d650da7ccd8f75d0f8d9')

    depends_on('r@3.00:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-progress', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-urltools', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
