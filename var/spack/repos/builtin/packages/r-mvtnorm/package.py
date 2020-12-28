# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMvtnorm(RPackage):
    """Computes multivariate normal and t probabilities, quantiles, random
    deviates and densities."""

    homepage = "http://mvtnorm.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/mvtnorm_1.0-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mvtnorm"

    version('1.0-11', sha256='0321612de99aa9bc75a45c7e029d3372736014223cbdefb80d8cae600cbc7252')
    version('1.0-10', sha256='31df19cd8b4cab9d9a70dba00442b7684e625d4ca143a2c023c2c5872b07ad12')
    version('1.0-6', sha256='4a015b57b645b520151b213eb04b7331598c06442a3f652c7dc149425bd2e444')
    version('1.0-5', sha256='d00f9f758f0d0d4b999f259223485dc55d23cbec09004014816f180045ac81dd')

    depends_on('r@1.9.0:', when='@:1.0-8', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@1.0-9:', type=('build', 'run'))
