# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class REllipsis(RPackage):
    """Tools for Working with ...

    The ellipsis is a powerful tool for extending functions. Unfortunately
    this power comes at a cost: misspelled arguments will be silently ignored.
    The ellipsis package provides a collection of functions to catch problems
    and alert the user."""

    homepage = "https://github.com/r-lib/ellipsis"
    url      = "https://cloud.r-project.org/src/contrib/ellipsis_0.2.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ellipsis"

    version('0.3.1', sha256='4f8a15158dfc27cdc0f7554c7a61e92b02e4d70bfc3d968f01a99da2189b75db')
    version('0.3.0', sha256='0bf814cb7a1f0ee1f2949bdc98752a0d535f2a9489280dd4d8fcdb10067ee907')
    version('0.2.0.1', sha256='0e6528c5e8016c3617cc1cfcdb5a4bfeb073e0bd5ea76b43e56b0c3208a0a943')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r@3.2:', when='@0.3:', type=('build', 'run'))
    depends_on('r-rlang@0.3.0:', type=('build', 'run'))
