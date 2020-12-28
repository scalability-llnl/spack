# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMaps(RPackage):
    """Display of maps. Projection code and larger maps are in separate
    packages ('mapproj' and 'mapdata')."""

    homepage = "https://cloud.r-project.org/package=maps"
    url      = "https://cloud.r-project.org/src/contrib/maps_3.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/maps"

    version('3.3.0', sha256='199afe19a4edcef966ae79ef802f5dcc15a022f9c357fcb8cae8925fe8bd2216')
    version('3.2.0', sha256='437abeb4fa4ad4a36af6165d319634b89bfc6bf2b1827ca86c478d56d670e714')
    version('3.1.1', sha256='972260e5ce9519ecc09b18e5d7a28e01bed313fadbccd7b06c571af349cb4d2a')

    depends_on('r@3.0.0:', type=('build', 'run'))
