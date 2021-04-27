# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRenv(RPackage):
    """Project Environments for R packages:

    A dependency management toolkit for R. Using 'renv', you can create and
    manage project-local R libraries, save the state of these libraries to a
    'lockfile', and later restore your library as required. Together, these
    tools can help make your projects more isolated, portable, and
    reproducible."""

    homepage = "https://rstudio.github.io/renv/"
    cran     = "renv"

    version('0.13.2', sha256='41f208ed957e27c50cbd8b0fff77a434bad963707df85e462419e2edb6719a4a')
