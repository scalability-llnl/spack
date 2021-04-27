# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RLeafletProviders(RPackage):
    """Leaflet Providers

    Contains third-party map tile provider information from 'Leaflet.js',
    <https://github.com/leaflet-extras/leaflet-providers>, to be used with the
    'leaflet' R package. Additionally, 'leaflet.providers' enables users to
    retrieve up-to-date provider information between package updates."""

    homepage = "https://github.com/rstudio/leaflet.providers"
    url      = "https://cloud.r-project.org/src/contrib/leaflet.providers_1.9.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/leaflet.providers"

    version('1.9.0', sha256='9e8fc75c83313ab24663c2e718135459599549ed6e7396086cacb44e36cfd67b')

    depends_on('r@2.10:', type=('build', 'run'))
