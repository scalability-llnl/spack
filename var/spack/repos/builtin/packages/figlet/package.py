# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Figlet(MakefilePackage):
    """FIGlet is a program that creates large characters out of ordinary
    screen characters."""

    homepage = "http://www.figlet.org/"
    url = "https://github.com/cmatsuoka/figlet/archive/2.2.5.tar.gz"

    license("BSD-3-Clause")

    version("2.2.5", sha256="4d366c4a618ecdd6fdb81cde90edc54dbff9764efb635b3be47a929473f13930")
    version("2.2.4", sha256="970a18a2a32cca736ff11a5b77e26a54f31a0e08606b85d21d3d5c666937e03d")
    version("2.2.3", sha256="168fa3c7a5888d6f796708780d3006f0e1871d83f32c4a10a84596b90ac35999")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        bins = ["figlet", "chkfont", "figlist", "showfigfonts"]
        for f in bins:
            install(f, prefix.bin)

        mkdirp(prefix.man6)
        manuals = ["figlet.6", "chkfont.6", "figlist.6", "showfigfonts.6"]
        for f in manuals:
            install(f, prefix.man6)

        install_tree("./fonts", prefix.share.figlet)

    @property
    def build_targets(self):
        return ["DEFAULTFONTDIR=" + self.prefix.share.figlet]
