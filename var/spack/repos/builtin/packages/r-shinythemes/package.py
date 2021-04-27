# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RShinythemes(RPackage):
    """Themes for Shiny:

    Themes for use with Shiny. Includes several Bootstrap themes from
    <https://bootswatch.com/>, which are packaged for use with Shiny
    applications."""

    homepage = "https://rstudio.github.io/shinythemes/"
    cran     = "shinythemes"

    version('1.2.0', sha256='37d68569ce838c7da9f0ea7e2b162ecf38fba2ae448a4888b6dd29c4bb5b2963')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-shiny@0.11:', type=('build', 'run'))
