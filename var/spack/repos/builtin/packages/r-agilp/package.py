# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAgilp(RPackage):
    """Agilent expression array processing package.

       More about what it does (maybe more than one line)"""

    homepage = "https://bioconductor.org/packages/agilp"
    git      = "https://git.bioconductor.org/packages/agilp.git"

    version('3.16.0', commit='2900d6066317f21d076b3a043b16f32eca168c47')
    version('3.14.0', commit='8feb047d70216013462ea7806e9227d192b60c61')
    version('3.12.0', commit='a86dea1b03b2b56c2c8317d4b10903fb8948ffcb')
    version('3.10.0', commit='cffec1004704a0c5119a50e3ad474897978981be')
    version('3.8.0', commit='c772a802af1b4c0741f2edd78053a0425160ea53')

    depends_on('r@2.14.0:', type=('build', 'run'))
