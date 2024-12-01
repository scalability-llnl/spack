# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfd(AutotoolsPackage, XorgPackage):
    """xfd - display all the characters in a font using either the
    X11 core protocol or libXft2."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xfd"
    xorg_mirror_path = "app/xfd-1.1.2.tar.gz"

    license("X11")

    version("1.1.4", sha256="58d3c4e1395a1d901529b1d80331d810836cb56b2db950c15444ea71d2af21fd")
    version("1.1.3", sha256="4a1bd18f324c239b1a807ed4ccaeb172ba771d65a7307fb492d8dd8d27f01527")
    version("1.1.2", sha256="4eff3e15b2526ceb48d0236d7ca126face399289eabc0ef67e6ed3b3fdcb60ad")

    depends_on("c", type="build")  # generated

    depends_on("fontconfig")
    depends_on("gettext")
    depends_on("libxaw")
    depends_on("libxft")
    depends_on("libxrender")
    depends_on("libxmu")
    depends_on("libxt")

    depends_on("xproto@7.0.17:")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    # Xfd requires libintl (gettext), but does not test for it
    # correctly, so add it here.
    def flag_handler(self, name, flags):
        if name == "ldlibs" and "intl" in self.spec["gettext"].libs.names:
            flags.append("-lintl")
        return self.inject_flags(name, flags)

    def configure_args(self):
        args = []

        # Xkb only rings a bell, so just disable it.
        if self.spec.satisfies("@1.1.3:"):
            args.append("--without-xkb")

        return args
