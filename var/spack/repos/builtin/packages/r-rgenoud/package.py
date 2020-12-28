# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgenoud(RPackage):
    """A genetic algorithm plus derivative optimizer."""

    homepage = "http://sekhon.berkeley.edu/rgenoud/"
    url      = "https://cloud.r-project.org/src/contrib/rgenoud_5.8-1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rgenoud"

    version('5.8-3.0', sha256='9beb11b5edab3ab3aa6001daa39668b240a8e0328be9d55db4e23ff88ce3235d')
    version('5.8-2.0', sha256='106c4f6a6df5159578e929a0141b3cfbaa88141a70703ff59a1fc48a27e2d239')
    version('5.8-1.0', sha256='9deca354be6887f56bf9f4ca9a7291296050e51149ae9a3b757501704126c38a')

    depends_on('r@2.15:', type=('build', 'run'))
