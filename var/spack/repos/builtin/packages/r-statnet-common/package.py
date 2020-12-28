# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStatnetCommon(RPackage):
    """Non-statistical utilities used by the software developed by the
       Statnet Project. They may also be of use to others."""

    homepage = "http://www.statnet.org"
    url      = "https://cloud.r-project.org/src/contrib/statnet.common_3.3.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/statnet.common"

    version('4.3.0', sha256='834a3359eac967df0420eee416ae4983e3b502a3de56bb24f494a7ca4104e959')
    version('4.2.0', sha256='1176c3303436ebe858d02979cf0a0c33e4e2d1f3637516b4761d573ccd132461')
    version('3.3.0', sha256='d714c4e7b0cbf71b7a628af443f5be530e74ad1e21f6b04f1b1087f6d7e40fa4')

    depends_on('r@3.5:', when='@4.2.0:', type=('build', 'run'))
    depends_on('r-coda', when='@4.1.2:', type=('build', 'run'))
