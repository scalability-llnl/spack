# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minisign(CMakePackage):
    """Minisign is a dead simple tool to sign files and verify signatures."""

    homepage = "https://jedisct1.github.io/minisign/"
    url = "https://github.com/jedisct1/minisign/archive/0.7.tar.gz"

    version('0.7', sha256='0c9f25ae647b6ba38cf7e6aea1da4e8fb20e1bc64ef0c679da737a38c8ad43ef')

    depends_on('libsodium')
