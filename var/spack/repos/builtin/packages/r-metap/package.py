# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RMetap(RPackage):
    """Meta-Analysis of Significance Values

    The canonical way to perform meta-analysis involves using effect sizes.
    When they are not available this package provides a number of methods for
    meta-analysis of significance values including the methods of Edgington,
    Fisher, Lancaster, Stouffer, Tippett, and Wilkinson; a number of data-sets
    to replicate published results; and a routine for graphical display."""

    homepage = "http://www.dewey.myzen.co.uk/meta/meta.html"
    url      = "https://cloud.r-project.org/src/contrib/metap_1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/metap"

    version('1.4', sha256='5fac23d823d0ad4eebc3f97620364e25f7b41f8d0c3579f6c09ec059940b85a5')
    version('1.1', sha256='20120428672d39dc15829c7e66850fc4350a34df290d48cef0b1cc78d13f7b82')

    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-rdpack', type=('build', 'run'))
    depends_on('r-rdpack@0.7:', when='@1.4:', type=('build', 'run'))
    depends_on('r-tfisher', when='@1.4:', type=('build', 'run'))
    depends_on('r-mutoss', when='@1.4:', type=('build', 'run'))
    depends_on('r-mathjaxr@0.8-3:', when='@1.4:', type=('build', 'run'))
