# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRvest(RPackage):
    """Wrappers around the 'xml2' and 'httr' packages to make it easy to
       download, then manipulate, HTML and XML."""

    homepage = "https://github.com/hadley/rvest"
    url      = "https://cloud.r-project.org/src/contrib/rvest_0.3.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rvest"

    version('0.3.4', sha256='413e171b9e89b7dc4e8b41165027cf19eb97cd73e149c252237bbdf0d0a4254a')
    version('0.3.3', sha256='b10a87fa2d733f7c0fc567242ef0ab10a1a77d58d51796996cc0fd81381a556f')
    version('0.3.2', sha256='0d6e8837fb1df79b1c83e7b48d8f1e6245f34a10c4bb6952e7bec7867e4abb12')

    depends_on('r@3.0.1:', when='@:0.3.2', type=('build', 'run'))
    depends_on('r@3.1:', when='@0.3.3', type=('build', 'run'))
    depends_on('r@3.2:', when='@0.3.4:', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
    depends_on('r-httr@0.5:', type=('build', 'run'))
    depends_on('r-selectr', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
