# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgsci(RPackage):
    """ggsci: Scientific Journal and Sci-Fi Themed Color Palettes for
    'ggplot2'"""

    homepage = "https://github.com/road2stat/ggsci"
    url      = "https://cloud.r-project.org/src/contrib/ggsci_2.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggsci"

    version('2.9', sha256='4af14e6f3657134c115d5ac5e65a2ed74596f9a8437c03255447cd959fe9e33c')
    version('2.8', sha256='b4ce7adce7ef23edf777866086f98e29b2b45b58fed085bbd1ffe6ab52d74ae8')
    version('2.4', sha256='9682c18176fee8e808c68062ec918aaef630d4d833e7a0bd6ae6c63553b56f00')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-ggplot2@2.0.0:', type=('build', 'run'))
