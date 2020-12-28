# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVfs(RPackage):
    """VFS: Vegetated Filter Strip and Erosion Model"""

    homepage = "https://cloud.r-project.org/package=VFS"
    url      = "https://cloud.r-project.org/src/contrib/VFS_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/VFS"

    version('1.0.2', sha256='8ff7e7e13919ff21f10c7c693ef596a2c7b57c7ca37d79278e443ed122a21aad')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-nleqslv@3.3.0:', type=('build', 'run'))
