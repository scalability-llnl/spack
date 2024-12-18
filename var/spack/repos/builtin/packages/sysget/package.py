# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Sysget(MakefilePackage):
    """sysget is a bridge that lets you use one syntax to every
    package manager on every unix-based operating system."""

    homepage = "https://github.com/emilengler/sysget"
    url = "https://github.com/emilengler/sysget/archive/v2.3.tar.gz"

    license("GPL-3.0-only")

    version("2.3", sha256="bba647bfd7093d18ee2b471a79f0cc50d84846aa3a04d790244acfefded79477")
    version("2.2", sha256="8f55ee8402d6de3cc16fa0577148b484e35da6688ad5f3ee3e9c1be04c88863a")
    version("2.1", sha256="0590aaae10494ca76c6749264925feb0e40b6e4b3822a8a4d148761addcb66c1")

    depends_on("cxx", type="build")  # generated

    def edit(self, spec, prefix):
        if os.path.exists("Makefile"):
            makefile = FileFilter("Makefile")
        elif os.path.exists("makefile"):
            makefile = FileFilter("makefile")

        makefile.filter(r"/usr/local/bin", self.prefix.bin)
        makefile.filter(r"/usr/local/man", self.prefix.man)
        makefile.filter(r"/etc", self.prefix.etc)

    @run_before("install")
    def create_install_directory(self):
        mkdirp(join_path(self.prefix, "bin"))
        mkdirp(join_path(self.prefix, "man"))
        mkdirp(join_path(self.prefix, "etc", "bash_completion.d"))
