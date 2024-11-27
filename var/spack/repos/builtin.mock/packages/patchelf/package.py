# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Patchelf(AutotoolsPackage):
    """PatchELF is a small utility to modify the dynamic linker and RPATH of
    ELF executables."""

    homepage = "https://nixos.org/patchelf.html"
    url = "https://nixos.org/releases/patchelf/patchelf-0.10/patchelf-0.10.tar.gz"
    list_url = "https://nixos.org/releases/patchelf/"
    list_depth = 1

    version("0.10", sha256="b2deabce05c34ce98558c0efb965f209de592197b2c88e930298d740ead09019")
    version("0.9", sha256="f2aa40a6148cb3b0ca807a1bf836b081793e55ec9e5540a5356d800132be7e0a")
    version("0.8", sha256="14af06a2da688d577d64ff8dac065bb8903bbffbe01d30c62df7af9bf4ce72fe")

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
