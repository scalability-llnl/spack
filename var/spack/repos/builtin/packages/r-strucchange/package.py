# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStrucchange(RPackage):
    """Testing, monitoring and dating structural changes in (linear)
    regression models."""

    homepage = "https://cloud.r-project.org/package=strucchange"
    url      = "https://cloud.r-project.org/src/contrib/strucchange_1.5-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/strucchange"

    version('1.5-1', sha256='740e2e20477b9fceeef767ae1002adc5ec397cb0f7daba5289a2c23b0dddaf31')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-sandwich', type=('build', 'run'))
