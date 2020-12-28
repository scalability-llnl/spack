# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRoxygen2(RPackage):
    """A 'Doxygen'-like in-source documentation system for Rd, collation, and
    'NAMESPACE' files."""

    homepage = "https://github.com/klutometis/roxygen"
    url      = "https://cloud.r-project.org/src/contrib/roxygen2_5.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/roxygen2"

    version('7.1.0', sha256='7e9b36f6e7c01a5c8c4747340b3d0c064ce2e48c93fcfbfe45139854fae74103')
    version('6.1.1', sha256='ed46b7e062e0dfd8de671c7a5f6d120fb2b720982e918dbeb01e6985694c0273')
    version('5.0.1', sha256='9f755ddd08358be436f08b02df398e50e7508b856131aeeed235099bb3a7eba5')

    depends_on('r@3.0.2:', when='@:6.0.1', type=('build', 'run'))
    depends_on('r@3.2:', when='@7.1.0:', type=('build', 'run'))
    depends_on('r@3.1:', when='@6.1.0:', type=('build', 'run'))
    depends_on('r-brew', type=('build', 'run'))
    depends_on('r-commonmark', type=('build', 'run'))
    depends_on('r-desc@1.2.0:', type=('build', 'run'))
    depends_on('r-knitr', when='@7.1.0:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-pkgload@1.0.2:', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-purrr@0.3.3:', when='@7.1.0:', type=('build', 'run'))
    depends_on('r-r6@2.1.2:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@7.1.0:', type=('build', 'run'))
    depends_on('r-stringi', type=('build', 'run'))
    depends_on('r-stringr@1.0.0:', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
