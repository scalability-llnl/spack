# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kdiff3(Package):
    """Compare and merge 2 or 3 files or directories."""

    homepage = "https://kdiff3.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/kdiff3/kdiff3/0.9.98/kdiff3-0.9.98.tar.gz"

    license("GPL-2.0-or-later")

    version("0.9.98", sha256="802c1ababa02b403a5dca15955c01592997116a24909745016931537210fd668")

    depends_on("cxx", type="build")  # generated

    depends_on("qt@:4,5.2.0:")

    def install(self, spec, prefix):
        # make is done inside
        configure("qt4")

        # there is no make install, bummer...
        mkdirp(self.prefix.bin)
        install(join_path(self.stage.source_path, "releaseQt", "kdiff3"), self.prefix.bin)
