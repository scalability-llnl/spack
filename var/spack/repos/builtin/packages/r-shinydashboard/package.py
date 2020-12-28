# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RShinydashboard(RPackage):
    """Create Dashboards with 'Shiny'"""

    homepage = "https://cloud.r-project.org/package=shinydashboard"
    url      = "https://cloud.r-project.org/src/contrib/shinydashboard_0.7.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/shinydashboard"

    version('0.7.1', sha256='51a49945c6b8a684111a2ba4b2a5964e3a50610286ce0378e37ae02316620a4e')
    version('0.7.0', sha256='0b7b102e9e5bea78ddc4da628d072a358270f2db9b63a6ebe4d8bdce3066d883')
    version('0.6.1', sha256='1ee38f257433d24455426bc9d85c36f588735a54fbf6143935fed9cccb3bf193')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-htmltools@0.2.6:', type=('build', 'run'))
    depends_on('r-shiny@1.0.0:', type=('build', 'run'))
    depends_on('r-promises', when='@0.7.1:', type=('build', 'run'))
