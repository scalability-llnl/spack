# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGridgraphics(RPackage):
    """gridGraphics: Redraw Base Graphics Using 'grid' Graphics"""

    homepage = "https://github.com/pmur002/gridgraphics"
    url      = "https://cloud.r-project.org/src/contrib/gridGraphics_0.4-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gridGraphics"

    version('0.4-1', sha256='b770127b71664bbf67f8853a2666c071f2b9920743eddc9f3a58ecb948b923cf')
