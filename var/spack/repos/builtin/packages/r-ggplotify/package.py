# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgplotify(RPackage):
    """ggplotify: Convert Plot to 'grob' or 'ggplot' Object"""

    homepage = "https://github.com/GuangchuangYu/ggplotify"
    url      = "https://cloud.r-project.org/src/contrib/ggplotify_0.0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggplotify"

    version('0.0.3', sha256='7e7953a2933aa7127a0bac54375e3e0219a0744cfc3249c3d7b76065f7a51892')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gridgraphics', type=('build', 'run'))
    depends_on('r-rvcheck', type=('build', 'run'))
