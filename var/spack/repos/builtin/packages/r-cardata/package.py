# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCardata(RPackage):
    """Datasets to Accompany J. Fox and S. Weisberg, An R Companion to Applied
    Regression, Third Edition, Sage (forthcoming)."""

    homepage = "https://r-forge.r-project.org/projects/car/"
    url      = "https://cloud.r-project.org/src/contrib/carData_3.0-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/carData"

    version('3.0-2', sha256='3b5c4eff1cc1e456a5331084774503eaa06cf61fb7acf6b9e8a6bfabd5735494')

    depends_on('r@3.0:', type=('build', 'run'))
