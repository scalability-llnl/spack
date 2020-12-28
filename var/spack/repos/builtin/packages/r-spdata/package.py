# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpdata(RPackage):
    """spData: Datasets for Spatial Analysis"""

    homepage = "https://github.com/Nowosad/spData"
    url      = "https://cloud.r-project.org/src/contrib/spData_0.3.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spData"

    version('0.3.0', sha256='de24ea659541a6c795cd26a1f6a213e15061af9c97a24cba1c24ce30c6c24c98')

    depends_on('r@3.3.0:', type=('build', 'run'))
