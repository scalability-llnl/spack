# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAda(RPackage):
    """Performs discrete, real, and gentle boost under both exponential
    and logistic loss on a given data set."""

    homepage = "https://cloud.r-project.org/package=ada"
    url      = "https://cloud.r-project.org/src/contrib/ada_2.0-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ada"

    version('2.0-5', sha256='d900172059eebeef30c27944fc29737a231fc4f92e3c2661868383fbd9016ac0')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-rpart', type=('build', 'run'))
