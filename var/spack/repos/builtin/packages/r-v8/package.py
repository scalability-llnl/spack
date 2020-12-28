# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RV8(RPackage):
    """V8: Embedded JavaScript and WebAssembly Engine for R"""

    homepage = "https://github.com/jeroen/v8"
    url      = "https://cloud.r-project.org/src/contrib/V8_3.4.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/V8"

    version('3.4.0', sha256='f5c8a2a03cc1be9f504f47711a0fcd1b962745139c9fb2a10fbd79c4ae103fbd')

    depends_on('r-curl@1.0:', type=('build', 'run'))
    depends_on('r-jsonlite@1.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.12:', type=('build', 'run'))
