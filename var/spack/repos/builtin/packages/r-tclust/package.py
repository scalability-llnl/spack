# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTclust(RPackage):
    """Provides functions for robust trimmed clustering."""

    homepage = "https://cloud.r-project.org/package=tclust"
    url      = "https://cloud.r-project.org/src/contrib/tclust_1.3-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tclust"

    version('1.4-1', sha256='4b0be612c8ecd7b4eb19a44ab6ac8f5d40515600ae1144c55989b6b41335ad9e')
    version('1.3-1',  sha256='fe4479a73b947d8f6c1cc63587283a8b6223d430d39eee4e5833a06d3d1726d2')
    version('1.2-7',  sha256='7d2cfa35bbd44086af45be842e6c4743380c7cc8a0f985d2bb7c1a0690c878d7')
    version('1.2-3',  sha256='d749d4e4107b876a22ca2c0299e30e2c77cb04f53f7e5658348e274aae3f2b28')
    version('1.1-03', sha256='b8a62a1d27e69ac7e985ba5ea2ae5d182d2e51665bfbfb178e22b63041709270')
    version('1.1-02', sha256='f73c0d7a495552f901b710cf34e114c0ba401d5a17c48156313245904bcccad4')

    depends_on('r@2.12.0:', type=('build', 'run'))
