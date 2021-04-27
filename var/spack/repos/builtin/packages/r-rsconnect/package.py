# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRsconnect(RPackage):
    """Deployment Interface for R Markdown Documents and Shiny Applications:

    Programmatic deployment interface for 'RPubs', 'shinyapps.io', and 'RStudio
    Connect'. Supported content types include R Markdown documents, Shiny
    applications, Plumber APIs, plots, and static web content."""

    homepage = "https://github.com/rstudio/rsconnect"
    cran     = "rsconnect"

    version('0.8.17', sha256='64767a4d626395b7871375956a9f0455c3d64ff6e779633b0e554921d85da231')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-openssl', type=('build', 'run'))
    depends_on('r-packrat@0.5:', type=('build', 'run'))
    depends_on('r-rstudioapi@0.5:', type=('build', 'run'))
    depends_on('r-yaml@2.1.5:', type=('build', 'run'))
