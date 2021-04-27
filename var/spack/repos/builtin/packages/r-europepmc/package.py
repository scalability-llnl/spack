# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class REuropepmc(RPackage):
    """R Interface to the Europe PubMed Central RESTful Web Service

    An R Client for the Europe PubMed Central RESTful Web Service (see
    <https://europepmc.org/RestfulWebService> for more information). It gives
    access to both metadata on life science literature and open access full
    texts. Europe PMC indexes all PubMed content and other literature sources
    including Agricola, a bibliographic database of citations to the
    agricultural literature, or Biological Patents. In addition to
    bibliographic metadata, the client allows users to fetch citations and
    reference lists. Links between life-science literature and other EBI
    databases, including ENA, PDB or ChEMBL are also accessible. No
    registration or API key is required. See the vignettes for usage
    examples."""

    homepage = "http://github.com/ropensci/europepmc/"
    url      = "https://cloud.r-project.org/src/contrib/europepmc_0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/europepmc"

    version('0.4', sha256='d55f62963d0ee84830654bbc78f4ad8285e376b04be137cbeaf8ad2a98b7969c')
    version('0.3', sha256='5044a253d223e2bb8502063cd03c0fe4db856467e497d650da7ccd8f75d0f8d9')

    depends_on('r@3.00:', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-progress', type=('build', 'run'))
    depends_on('r-urltools', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
    depends_on('r-tibble', when='@0.4:', type=('build', 'run'))
    depends_on('r-tidyr', when='@0.4:', type=('build', 'run'))
    depends_on('r-rlang', when='@0.4:', type=('build', 'run'))
