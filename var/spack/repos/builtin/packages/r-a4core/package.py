# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RA4core(RPackage):
    """Automated Affymetrix Array Analysis Core Package."""

    homepage = "https://bioconductor.org/packages/a4Core"
    git      = "https://git.bioconductor.org/packages/a4Core.git"

    version('1.32.0', commit='2916a29723bdd514d5d987f89725d141d1d2dfce')
    version('1.30.0', commit='e392b1b4339a34f93d5d9bc520a1a9385ea63141')
    version('1.28.0', commit='39b6ee29bc2f2fdc5733438c14dc02f8abc6460b')
    version('1.26.0', commit='e7be935f20b486165a2b27dbbf9e99ba07151bcd')
    version('1.24.0', commit='c871faa3e1ab6be38a9ea3018816cf31b58b0ed3')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-glmnet', type=('build', 'run'))
