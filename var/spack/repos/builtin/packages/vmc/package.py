# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vmc(CMakePackage):
    """The Virtual Monte Carlo (VMC) library"""

    homepage = "https://github.com/vmc-project/vmc"
    git      = 'https://github.com/vmc-project/vmc.git'
    url      = "https://github.com/vmc-project/vmc/archive/v1-0-p3.tar.gz"

    maintainers = ['ChristianTackeGSI']

    version('1-0-p3', sha256='46385776d7639fdf23df2a2a5426fb9a9a69836d237c1259b1a22bfb649cb47e')
    version('1-0-p2', sha256='46b4c82b0b7516502e88db920732fc78f06f0393ac740a17816f2eb53f80e75e')
    version('1-0-p1', sha256='4a20515f7de426797955cec4a271958b07afbaa330770eeefb5805c882ad9749')

    patch('dict_fixes_101.patch', when='@1-0-p1')

    depends_on('root@6.18.04: ~vmc')
