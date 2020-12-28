# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGamlssData(RPackage):
    """gamlss.data: GAMLSS Data"""

    homepage = "https://cloud.r-project.org/package=gamlss.data"
    url      = "https://cloud.r-project.org/src/contrib/gamlss.data_5.1-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gamlss.data/"

    version('5.1-4', sha256='0d3777d8c3cd76cef273aa6bde40a91688719be401195ed9bfd1e85bd7d5eeb5')
    version('5.1-3', sha256='4941180e7eebe97678ba02ca24c2a797bcb69d92cd34600215a94110e2a70470')
    version('5.1-0', sha256='0aad438ea1aa6395677e52cd2cb496f9f4c9ba2d39edc92c8cb42e7fc91fe6c1')

    depends_on('r@2.10:', type=('build', 'run'))
