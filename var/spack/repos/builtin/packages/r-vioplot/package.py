# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVioplot(RPackage):
    """vioplot: Violin Plot"""

    homepage = "https://cloud.r-project.org/package=vioplot"
    url      = "https://cloud.r-project.org/src/contrib/vioplot_0.3.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/vioplot"

    version('0.3.2', sha256='7b51d0876903a3c315744cb051ac61920eeaa1f0694814959edfae43ce956e8e')

    depends_on('r-sm', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
