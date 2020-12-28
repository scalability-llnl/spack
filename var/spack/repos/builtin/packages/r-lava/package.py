# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLava(RPackage):
    """Estimation and simulation of latent variable models."""

    homepage = "https://cloud.r-project.org/package=lava"
    url      = "https://cloud.r-project.org/src/contrib/lava_1.4.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lava"

    version('1.6.6', sha256='7abc84dd99cce450a45ac4f232812cde3a322e432da3472f43b057fb5c59ca59')
    version('1.6.4', sha256='41c6eeb96eaef9e1bfb04b31f7203e250a5ea7e7860be4d95f7f96f2a8644718')
    version('1.4.7', sha256='d5cbd4835a94855478efb93051eece965db116ead203f4dd4e09d9a12d52f4bf')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-squarem', when='@1.6.0:', type=('build', 'run'))
