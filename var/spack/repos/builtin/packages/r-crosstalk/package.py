# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCrosstalk(RPackage):
    """Provides building blocks for allowing HTML widgets to communicate with
    each other, with Shiny or without (i.e. static .html files)."""

    homepage = "https://cloud.r-project.org/package=crosstalk"
    url      = "https://cloud.r-project.org/src/contrib/crosstalk_1.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/crosstalk"

    version('1.0.0', sha256='b31eada24cac26f24c9763d9a8cbe0adfd87b264cf57f8725027fe0c7742ca51')

    depends_on('r-htmltools@0.3.5:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-shiny@0.11:', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
