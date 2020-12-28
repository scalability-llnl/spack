# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScatterplot3d(RPackage):
    """scatterplot3d: 3D Scatter Plot"""

    homepage = "https://cloud.r-project.org/package=scatterplot3d"
    url      = "https://cloud.r-project.org/src/contrib/scatterplot3d_0.3-40.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/scatterplot3d"

    version('0.3-41', sha256='4c8326b70a3b2d37126ca806771d71e5e9fe1201cfbe5b0d5a0a83c3d2c75d94')
    version('0.3-40', sha256='8249118aa29199017a6686d8245fed5343dabcf049b1588141a7cf83245b6a29')

    depends_on('r@2.7.0:', type=('build', 'run'))
