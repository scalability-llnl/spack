# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Miniasm(MakefilePackage):
    """Miniasm is a very fast OLC-based de novo assembler for noisy long
    reads."""

    homepage = "http://www.example.co://github.com/lh3/miniasm"
    git      = "https://github.com/lh3/miniasm.git"

    version('2018-3-30', commit='55cf0189e2f7d5bda5868396cebe066eec0a9547')

    depends_on('zlib')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
