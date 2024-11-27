# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aeskeyfind(MakefilePackage):
    """This program illustrates automatic techniques for locating 128-bit
    and 256-bit AES keys in a captured memory image."""

    homepage = "https://github.com/makomk/aeskeyfind"
    git = "https://github.com/makomk/aeskeyfind.git"

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("aeskeyfind", prefix.bin)
