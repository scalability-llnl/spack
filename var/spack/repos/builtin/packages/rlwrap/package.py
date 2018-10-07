# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rlwrap(AutotoolsPackage):
    """rlwrap is a 'readline wrapper', a small utility that uses the GNU
    readline library to allow the editing of keyboard input for any command."""

    homepage = "https://github.com/hanslub42/rlwrap"
    url      = "https://github.com/hanslub42/rlwrap/releases/download/v0.43/rlwrap-0.43.tar.gz"

    version('0.43', 'b993e83d3a292464de70719b32f83a34')

    depends_on('readline@4.2:')
