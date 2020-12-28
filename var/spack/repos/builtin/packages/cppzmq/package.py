# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppzmq(CMakePackage):
    """C++ binding for 0MQ"""

    homepage = "http://www.zeromq.org"
    url      = "https://github.com/zeromq/cppzmq/archive/v4.2.2.tar.gz"
    git      = "https://github.com/zeromq/cppzmq.git"

    version('master', branch='master')
    version('4.6.0', sha256='e9203391a0b913576153a2ad22a2dc1479b1ec325beb6c46a3237c669aef5a52')
    version('4.5.0', sha256='64eb4e58eaf0c77505391c6c9a606cffcb57c6086f3431567a1ef4a25b01fa36')
    version('4.4.1', sha256='117fc1ca24d98dbe1a60c072cde13be863d429134907797f8e03f654ce679385')
    version('4.4.0', sha256='118b9ff117f07d1aabadfb905d7227362049d7940d16b7863b3dd3cebd28be85')
    version('4.3.0', sha256='27d1f56406ba94ee779e639203218820975cf68174f92fbeae0f645df0fcada4')
    version('4.2.3', sha256='3e6b57bf49115f4ae893b1ff7848ead7267013087dc7be1ab27636a97144d373')
    version('4.2.2', sha256='3ef50070ac5877c06c6bb25091028465020e181bbfd08f110294ed6bc419737d')

    depends_on('cmake@3.0.0:', type='build')
    depends_on('libzmq')
    depends_on('libzmq@4.2.2', when='@4.2.2:4.2.3')

    def cmake_args(self):
        args = []
        # https://github.com/zeromq/cppzmq/issues/422
        # https://github.com/zeromq/cppzmq/pull/288
        args.append('-DCPPZMQ_BUILD_TESTS=OFF')
        return args
