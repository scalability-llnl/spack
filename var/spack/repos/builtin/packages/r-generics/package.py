# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGenerics(RPackage):
    """Common S3 Generics not Provided by Base R Methods Related to Model Fitting

    In order to reduce potential package dependencies and conflicts,
    generics provides a number of commonly used S3 generics."""

    homepage = "https://github.com/r-lib/generics"
    url      = "https://cloud.r-project.org/src/contrib/generics_0.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/generics"

    version('0.1.0', sha256='ab71d1bdbb66c782364c61cede3c1186d6a94c03635f9af70d926e2c1ac88763')
    version('0.0.2', sha256='71b3d1b719ce89e71dd396ac8bc6aa5f1cd99bbbf03faff61dfbbee32fec6176')

    depends_on('r@3.1:', type=('build', 'run'))
