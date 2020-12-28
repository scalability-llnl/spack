# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVipor(RPackage):
    """Plot Categorical Data Using Quasirandom Noise and Density Estimates"""

    homepage = "https://cloud.r-project.org/package=vipor"
    url      = "https://cloud.r-project.org/src/contrib/vipor_0.4.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/vipor"

    version('0.4.5', sha256='7d19251ac37639d6a0fed2d30f1af4e578785677df5e53dcdb2a22771a604f84')
    version('0.4.4', sha256='5abfd7869dae42ae2e4f52206c23433a43b485b1220685e445877ee5864a3f5c')

    depends_on('r@3.0.0:', type=('build', 'run'))
