# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSfsmisc(RPackage):
    """Useful utilities ['goodies'] from Seminar fuer Statistik
    ETH Zurich, quite a few related to graphics;
    some were ported from S-plus."""

    homepage = "https://cloud.r-project.org/package=sfsmisc"
    url      = "https://cloud.r-project.org/src/contrib/sfsmisc_1.1-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sfsmisc"

    version('1.1-4', sha256='44b6a9c859922e86b7182e54eb781d3264f3819f310343518ebc66f54f305c7d')
    version('1.1-3', sha256='58eff7d4a9c79212321858efe98d2a6153630e263ff0218a31d5e104b8b545f8')
    version('1.1-0', sha256='7f430cf3ebb95bac806fbf093fb1e2112deba47416a93be8d5d1064b76bc0015')

    depends_on('r@3.0.1:', when='@:1.1-1', type=('build', 'run'))
    depends_on('r@3.2.0:', when='@1.1-2:', type=('build', 'run'))
