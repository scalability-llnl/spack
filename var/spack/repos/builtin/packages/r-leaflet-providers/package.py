# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLeafletProviders(RPackage):
    """Leaflet Providers.

    Contains third-party map tile provider information from 'Leaflet.js',
    <https://github.com/leaflet-extras/leaflet-providers>, to be used with the
    'leaflet' R package. Additionally, 'leaflet.providers' enables users to
    retrieve up-to-date provider information between package updates."""

    cran = "leaflet.providers"

    license("BSD-2-Clause")

    version("2.0.0", sha256="c5ceeadc8088c9840a8249f0347501cdba0119be97219a01ea2050d1dd4a8666")
    version("1.9.0", sha256="9e8fc75c83313ab24663c2e718135459599549ed6e7396086cacb44e36cfd67b")

    depends_on("r@2.10:", type=("build", "run"))

    depends_on("r-htmltools", type=("build", "run"), when="@2.0.0:")
