# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPolyclip(RPackage):
    """polyclip: Polygon Clipping"""

    homepage = "https://cloud.r-project.org/package=polyclip"
    url      = "https://cloud.r-project.org/src/contrib/polyclip_1.10-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/polyclip"

    version('1.10-0', sha256='74dabc0dfe5a527114f0bb8f3d22f5d1ae694e6ea9345912909bae885525d34b')

    depends_on('r@3.0.0:', type=('build', 'run'))
