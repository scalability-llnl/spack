# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RScattermore(RPackage):
    """Scatterplots with More Points

    C-based conversion of large scatterplot data to rasters. Speeds up plotting
    of data with millions of points."""

    homepage = "https://github.com/exaexa/scattermore"
    url      = "https://cloud.r-project.org/src/contrib/scattermore_0.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/scattermore"

    version('0.7', sha256='f36280197b8476314d6ce81a51c4ae737180b180204043d2937bc25bf3a5dfa2')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
