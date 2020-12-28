# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLeaps(RPackage):
    """leaps: Regression Subset Selection"""

    homepage = "https://cloud.r-project.org/package=leaps"
    url      = "https://cloud.r-project.org/src/contrib/leaps_3.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/leaps"

    version('3.0', sha256='55a879cdad5a4c9bc3b5697dd4d364b3a094a49d8facb6692f5ce6af82adf285')
