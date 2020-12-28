# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBookdown(RPackage):
    """Output formats and utilities for authoring books and technical
    documents with R Markdown."""

    homepage = "https://cloud.r-project.org/package=bookdown"
    url      = "https://cloud.r-project.org/src/contrib/bookdown_0.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bookdown"

    version('0.12', sha256='38eb4c5b877ccd85b16cfe74a48c3bc53de2f276da98e5515f37e7a06e065bb0')
    version('0.5', sha256='b7331fd56f64bd2bddc34e2a188fc491f9ff5308f44f7e3151721247f21ca67e')

    depends_on('r-yaml@2.1.14:', when='@:0.10', type=('build', 'run'))
    depends_on('r-rmarkdown@1.12:', type=('build', 'run'))
    depends_on('r-knitr@1.22:', type=('build', 'run'))
    depends_on('r-htmltools@0.3.6:', type=('build', 'run'))
    depends_on('r-xfun@0.6:', when='@0.12:', type=('build', 'run'))
    depends_on('r-tinytex@0.12:', when='@0.12:', type=('build', 'run'))
    depends_on('pandoc@1.17.2:')
