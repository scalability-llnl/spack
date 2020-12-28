# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kentutils(MakefilePackage):
    """Jim Kent command line bioinformatic utilities"""

    homepage = "https://github.com/ENCODE-DCC/kentUtils"
    git      = "https://github.com/ENCODE-DCC/kentUtils.git"

    version('302.1', commit='d8376c5d52a161f2267346ed3dc94b5dce74c2f9')

    depends_on('libpng')
    depends_on('openssl')

    # Actually depends on mysql, but mariadb works for now until mysql is
    # available
    depends_on('mariadb')

    conflicts('%cce')
    conflicts('%apple-clang')
    conflicts('%clang')
    conflicts('%intel')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
