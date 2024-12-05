# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsixel(MesonPackage):
    """
    This package provides encoder/decoder implementation for DEC SIXEL graphics,
    and some converter programs like img2sixel.
    """

    homepage = "https://github.com/libsixel/libsixel"
    url = "https://github.com/libsixel/libsixel/archive/refs/tags/v1.10.3.tar.gz"

    maintainers("taliaferro")

    version("1.10.3", sha256="028552eb8f2a37c6effda88ee5e8f6d87b5d9601182ddec784a9728865f821e0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("img2sixel", default=True, description="build binary img2sixel")
    variant("sixel2png", default=True, description="build binary sixel2png")
    variant("gd", default=True, description="build with libgd")
    variant("jpeg", default=False, description="build with libjpeg")
    variant("png", default=False, description="build with libpng")
    variant("libcurl", default=False, description="build with libcurl")
    variant("gdk-pixbuf2", default=False, description="build with gdk-pixbuf2")

    depends_on("curl", when="+libcurl")
    depends_on("libgd", when="+gd")
    depends_on("gdk-pixbuf", when="+gdk-pixbuf2")
    depends_on("libjpeg", when="+jpeg")
    depends_on("libpng", when="+png")

    def meson_args(self):
        options = ["img2sixel", "sixel2png", "libcurl", "gdk-pixbuf2"]
        args = []
        for option in options:
            state = "enabled" if "+{}".format(option) in self.spec else "disabled"
            args.append("-D{option}={state}".format(option=option, state=state))
        return args
