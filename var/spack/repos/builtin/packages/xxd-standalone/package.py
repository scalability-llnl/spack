# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class XxdStandalone(MakefilePackage):
    """xxd creates a hex dump of a given file or standard input.
    It is bundled with vim, but as xxd is used in build scripts,
    it makes sense to have it available as a standalone package."""

    homepage = "https://www.vim.org/"
    url = "https://github.com/vim/vim/archive/v8.2.1201.tar.gz"

    maintainers("haampie")
    build_targets = ["-C", os.path.join("src", "xxd")]

    provides("xxd")

    license("Vim")

    version("8.2.1201", sha256="39032fe866f44724b104468038dc9ac4ff2c00a4b18c9a1e2c27064ab1f1143d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(os.path.join(self.build_directory, "src", "xxd", "xxd"), prefix.bin)
