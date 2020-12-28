# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMemoise(RPackage):
    """Cache the results of a function so that when you call it again with the
    same arguments it returns the pre-computed value."""

    homepage = "https://github.com/hadley/memoise"
    url      = "https://cloud.r-project.org/src/contrib/memoise_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/memoise"
    version('1.1.0', sha256='b276f9452a26aeb79e12dd7227fcc8712832781a42f92d70e86040da0573980c')
    version('1.0.0', sha256='fd1b6cf12929890db7819f74a44a1dbe3d6f25c8a608a956d827f8be2f6c026b')

    depends_on('r-digest@0.6.3:', type=('build', 'run'))
