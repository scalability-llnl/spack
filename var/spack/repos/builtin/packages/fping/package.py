# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fping(AutotoolsPackage):
    """High performance ping tool."""

    homepage = "https://fping.org/"
    url      = "https://github.com/schweikert/fping/archive/v4.2.tar.gz"

    version('4.2', sha256='49b0ac77fd67c1ed45c9587ffab0737a3bebcfa5968174329f418732dbf655d4')
    version('4.1', sha256='1da45b1d8c2d38b52bebd4f8b1617ddfae678e9f6436dafa6f62e97b8ecfc93c')
    version('4.0', sha256='8c9eac7aeadb5be0daa978cdac5f68ae44b749af0f643e8252b5e3dd4ce32e6a')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
