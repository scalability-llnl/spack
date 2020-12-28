# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCorpcor(RPackage):
    """Efficient Estimation of Covariance and (Partial) Correlation"""

    homepage = "https://cloud.r-project.org/package=corpcor"
    url      = "https://cloud.r-project.org/src/contrib/corpcor_1.6.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/corpcor"

    version('1.6.9', sha256='2e4fabd1d3936fecea67fa365233590147ca50bb45cf80efb53a10345a8a23c2')

    depends_on('r@3.0.2:', type=('build', 'run'))
