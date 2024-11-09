# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pacvim(MakefilePackage):
    """Pacvim is a command-line-based game based off of Pacman.
    The main purpose of this software is to familiarize individuals
    with Vim."""

    homepage = "https://github.com/jmoon018/PacVim"
    url = "https://github.com/jmoon018/PacVim/archive/v1.1.1.tar.gz"

    version("1.1.1", sha256="c869c5450fbafdfe8ba8a8a9bba3718775926f276f0552052dcfa090d21acb28")

    depends_on("cxx", type="build")  # generated

    depends_on("ncurses")

    def edit(self, stage, prefix):
        makefile = FileFilter("Makefile")

        makefile.filter(r"PREFIX = /usr/local", "PREFIX={0}".format(self.prefix))
