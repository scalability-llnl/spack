# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGooglevis(RPackage):
    """R interface to Google Charts API, allowing users to create interactive
    charts based on data frames. Charts are displayed locally via the R HTTP
    help server. A modern browser with an Internet connection is required and
    for some charts a Flash player. The data remains local and is not uploaded
    to Google."""

    homepage = "https://github.com/mages/googleVis#googlevis"
    url      = "https://cloud.r-project.org/src/contrib/googleVis_0.6.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/googleVis"

    version('0.6.4', sha256='7dcaf0e9d5e5598c17e8bd474141708de37eeb2578b09788431b9d871edb7eb8')
    version('0.6.3', sha256='17d104c5d4e6ab7b984df229cd51be19681e4726077afec7c61a33f6e4c0b6ef')
    version('0.6.0', sha256='862708097fbb5d4e83193777f40979d7848f9841d94d48ee8a74106266acc440')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
