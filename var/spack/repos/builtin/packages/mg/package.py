# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mg(MakefilePackage):
    """Mg is intended to be a small, fast, and portable editor for people
    who can't (or don't want to) run emacs for one reason or another,
    or are not familiar with the vi editor. It is compatible with
    emacs because there shouldn't be any reason to learn more editor
    types than emacs or vi."""

    homepage = "https://github.com/ibara/mg"
    url = "https://github.com/ibara/mg/archive/mg-6.6.tar.gz"

    version("6.6", sha256="e8440353da1a52ec7d40fb88d4f145da49c320b5ba31daf895b0b0db5ccd0632")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")

    def edit(self, spec, prefix):
        configure = Executable("./configure")
        args = ["--mandir={0}".format(self.prefix.man), "--prefix={0}".format(self.prefix)]
        configure(*args)
