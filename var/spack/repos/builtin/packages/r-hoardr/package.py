# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHoardr(RPackage):
    """hoardr: Manage Cached Files"""

    homepage = "https://cloud.r-project.org/package=hoardr"
    url      = "https://cloud.r-project.org/src/contrib/hoardr_0.5.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/hoardr/"

    version('0.5.2', sha256='819113f0e25da105f120a676b5173872a4144f2f6f354cad14b35f898e76dc54')

    depends_on('r-r6@2.2.0:', type=('build', 'run'))
    depends_on('r-rappdirs@0.3.1:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
