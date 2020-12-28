# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRferns(RPackage):
    """Provides the random ferns classifier"""

    homepage = "https://cloud.r-project.org/package=rFerns"
    url      = "https://cloud.r-project.org/src/contrib/rFerns_3.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rFerns"

    version('3.0.0', sha256='35e7e31a6497e415a0fe578678cf9b2f537b21319e4c015a1e2dade00310227c')
