# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDebugme(RPackage):
    """Specify debug messages as special string constants, and control
    debugging of packages via environment variables."""

    homepage = "https://github.com/r-lib/debugme#readme"
    url      = "https://cloud.r-project.org/src/contrib/debugme_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/debugme"

    version('1.1.0', sha256='4dae0e2450d6689a6eab560e36f8a7c63853abbab64994028220b8fd4b793ab1')

    depends_on('r-crayon', type=('build', 'run'))
