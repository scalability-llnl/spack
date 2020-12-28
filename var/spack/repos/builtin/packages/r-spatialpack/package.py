# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatialpack(RPackage):
    """Tools to assess the association between two spatial processes."""

    homepage = "https://cloud.r-project.org/package=SpatialPack"
    url      = "https://cloud.r-project.org/src/contrib/SpatialPack_0.3-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/SpatialPack"

    version('0.3-8', sha256='a0e54b5dee3cd30a634e2d30380fe163942b672073fd909be888803332ed5151')
    version('0.3',   sha256='4c80fc1c77bc97fc678e6e201ecf7f0f89dcf3417b3b497a28a3639e9b30bd8a')

    depends_on('r@2.10:', type=('build', 'run'))
