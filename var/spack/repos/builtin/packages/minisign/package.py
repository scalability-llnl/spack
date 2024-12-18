# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Minisign(CMakePackage):
    """Minisign is a dead simple tool to sign files and verify signatures."""

    homepage = "https://jedisct1.github.io/minisign/"
    url = "https://github.com/jedisct1/minisign/archive/0.7.tar.gz"

    maintainers("alalazo")

    license("ISC")

    version("0.11", sha256="74c2c78a1cd51a43a6c98f46a4eabefbc8668074ca9aa14115544276b663fc55")
    version("0.9", sha256="caa4b3dd314e065c6f387b2713f7603673e39a8a0b1a76f96ef6c9a5b845da0f")
    version("0.8", sha256="130eb5246076bc7ec42f13495a601382e566bb6733430d40a68de5e43a7f1082")
    version("0.7", sha256="0c9f25ae647b6ba38cf7e6aea1da4e8fb20e1bc64ef0c679da737a38c8ad43ef")

    depends_on("c", type="build")  # generated

    variant("static", default=True, description="builds a static version of the executable")

    depends_on("libsodium")

    def cmake_args(self):
        return [self.define_from_variant("STATIC_LIBSODIUM", "static")]
