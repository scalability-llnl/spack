# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPixmap(RPackage):
    """Bitmap Images ("Pixel Maps")

    Functions for import, export, plotting and other manipulations of bitmapped
    images."""

    homepage = "https://cloud.r-project.org/package=pixmap"
    url      = "https://cloud.r-project.org/src/contrib/pixmap_0.4-11.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pixmap"

    version('0.4-11', sha256='6fa010749a59cdf56aad9f81271473b7d55697036203f2cd5d81372bcded7412')
