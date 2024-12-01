# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppzmq(CMakePackage):
    """C++ binding for 0MQ"""

    homepage = "https://www.zeromq.org"
    url = "https://github.com/zeromq/cppzmq/archive/v4.2.2.tar.gz"
    git = "https://github.com/zeromq/cppzmq.git"

    maintainers("wdconinc")

    license("MIT")

    version("master", branch="master")
    version("4.10.0", sha256="c81c81bba8a7644c84932225f018b5088743a22999c6d82a2b5f5cd1e6942b74")
    version("4.9.0", sha256="3fdf5b100206953f674c94d40599bdb3ea255244dcc42fab0d75855ee3645581")
    version("4.8.1", sha256="7a23639a45f3a0049e11a188e29aaedd10b2f4845f0000cf3e22d6774ebde0af")
    version("4.7.1", sha256="9853e0437d834cbed5d3c223bf1d755cadee70e7c964c6e42c4c6783dee5d02c")
    version("4.6.0", sha256="e9203391a0b913576153a2ad22a2dc1479b1ec325beb6c46a3237c669aef5a52")
    version("4.5.0", sha256="64eb4e58eaf0c77505391c6c9a606cffcb57c6086f3431567a1ef4a25b01fa36")
    version("4.4.1", sha256="117fc1ca24d98dbe1a60c072cde13be863d429134907797f8e03f654ce679385")
    version("4.4.0", sha256="118b9ff117f07d1aabadfb905d7227362049d7940d16b7863b3dd3cebd28be85")
    version("4.3.0", sha256="27d1f56406ba94ee779e639203218820975cf68174f92fbeae0f645df0fcada4")
    version("4.2.3", sha256="3e6b57bf49115f4ae893b1ff7848ead7267013087dc7be1ab27636a97144d373")
    version("4.2.2", sha256="3ef50070ac5877c06c6bb25091028465020e181bbfd08f110294ed6bc419737d")

    depends_on("cxx", type="build")  # generated

    variant("drafts", default=False, description="Build and install draft classes and methods")

    depends_on("cmake@3.0.0:", type="build")
    depends_on("cmake@3.11:", type="build", when="@4.8:")
    depends_on("libzmq")
    depends_on("libzmq@4.2.2", when="@4.2.2:4.2.3")
    depends_on("libzmq+drafts", when="+drafts")

    def cmake_args(self):
        args = []

        args.append(self.define_from_variant("ENABLE_DRAFTS", "drafts"))

        # https://github.com/zeromq/cppzmq/issues/422
        # https://github.com/zeromq/cppzmq/pull/288
        args.append("-DCPPZMQ_BUILD_TESTS=OFF")
        return args
