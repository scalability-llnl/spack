# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWebshot(RPackage):
    """webshot: Take Screenshots of Web Pages"""

    homepage = "https://github.com/wch/webshot/"
    url      = "https://cloud.r-project.org/src/contrib/webshot_0.5.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/webshot/"

    version('0.5.1', sha256='b9750d206c6fa0f1f16cc212b0a34f4f4bfa916962d2c877f0ee9a33620f4b23')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-callr', type=('build', 'run'))
