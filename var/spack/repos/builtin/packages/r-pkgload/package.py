# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPkgload(RPackage):
    """pkgload: Simulate Package Installation and Attach"""

    homepage = "https://cloud.r-project.org/package=pkgload"
    url      = "https://cloud.r-project.org/src/contrib/pkgload_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pkgload/"

    version('1.0.2', sha256='3186564e690fb05eabe76e1ac0bfd4312562c3ac8794b29f8850399515dcf27c')

    depends_on('r-desc', type=('build', 'run'))
    depends_on('r-pkgbuild', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-rprojroot', type=('build', 'run'))
    depends_on('r-rstudioapi', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
