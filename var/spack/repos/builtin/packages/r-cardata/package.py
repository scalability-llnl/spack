# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCardata(RPackage):
    """Companion to Applied Regression Data Sets

    Datasets to Accompany J. Fox and S. Weisberg, An R Companion to Applied
    Regression, Third Edition, Sage (2019)."""

    homepage = "https://r-forge.r-project.org/projects/car/"
    url      = "https://cloud.r-project.org/src/contrib/carData_3.0-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/carData"

    version('3.0-4', sha256='cda6f5e3efc1d955a4a0625e9c33f90d49f5455840e88b3bd757129b86044724')
    version('3.0-2', sha256='3b5c4eff1cc1e456a5331084774503eaa06cf61fb7acf6b9e8a6bfabd5735494')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r@3.5:', when='@3.0-4:', type=('build', 'run'))
