# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMagic(RPackage):
    """A collection of efficient, vectorized algorithms for the creation and
    investigation of magic squares and hypercubes, including a variety of
    functions for the manipulation and analysis of arbitrarily dimensioned
    arrays."""

    homepage = "https://cloud.r-project.org/package=magic"
    url      = "https://cloud.r-project.org/src/contrib/magic_1.5-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/magic"

    version('1.5-9', sha256='fa1d5ef2d39e880f262d31b77006a2a7e76ea38e306aae4356e682b90d6cd56a')
    version('1.5-8', sha256='7f8bc26e05003168e9d2dadf64eb9a34b51bc41beba482208874803dee7d6c20')
    version('1.5-6', sha256='1b6c3f5bef0ddc28c4b68894051df5d9c0d4985d9e6ad81892369d0f7fe0298d')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-abind', type=('build', 'run'))
