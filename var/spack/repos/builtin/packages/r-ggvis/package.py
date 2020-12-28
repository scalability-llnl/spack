# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgvis(RPackage):
    """An implementation of an interactive grammar of graphics, taking the best
    parts of 'ggplot2', combining them with the reactive framework from 'shiny'
    and web graphics from 'vega'."""

    homepage = "http://ggvis.rstudio.com/"
    url      = "https://cloud.r-project.org/src/contrib/ggvis_0.4.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggvis"

    version('0.4.4', sha256='1332ea122b768688c8a407a483be80febc4576de0ec8929077738421b27cafaf')
    version('0.4.3', sha256='34d517783016aaa1c4bef8972f4c06df5cd9ca0568035b647e60a8369043ecdc')
    version('0.4.2', sha256='2fcc2b6ca4fbdc69fe75a2c58c12cb43096ab418160c98367e5ac0fd19fc591d')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-jsonlite@0.9.11:', type=('build', 'run'))
    depends_on('r-shiny@0.11.1:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-dplyr@0.4.0:', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-htmltools@0.2.4:', type=('build', 'run'))
