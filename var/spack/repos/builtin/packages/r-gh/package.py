# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGh(RPackage):
    """Minimal client to access the 'GitHub' 'API'."""

    homepage = "https://github.com/r-lib/gh#readme"
    url      = "https://cloud.r-project.org/src/contrib/gh_1.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gh"

    version('1.1.0', sha256='de9faf383c3fe5e87a75391d82cf71b1331b3c80cd00c4203146a303825d89ad')
    version('1.0.1', sha256='f3c02b16637ae390c3599265852d94b3de3ef585818b260d00e7812595b391d2')

    depends_on('r-ini', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-httr@1.2:', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-cli', when='@1.1.0:', type=('build', 'run'))
