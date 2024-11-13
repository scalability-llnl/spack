# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mkfontscale(AutotoolsPackage, XorgPackage):
    """mkfontscale creates the fonts.scale and fonts.dir index files used by the
    legacy X11 font system."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/mkfontscale"
    xorg_mirror_path = "app/mkfontscale-1.1.2.tar.gz"

    license("MIT")

    version("1.2.3", sha256="3a026b468874eb672a1d0a57dbd3ddeda4f0df09886caf97d30097b70c2df3f8")
    version("1.2.2", sha256="4a5af55e670713024639a7f7d10826d905d86faf574cd77e0f5aef2d00e70168")
    version("1.1.2", sha256="8bba59e60fbc4cb082092cf6b67e810b47b4fe64fbc77dbea1d7e7d55312b2e4")

    depends_on("c", type="build")

    depends_on("libfontenc")
    depends_on("freetype build_system=autotools")

    depends_on("xproto@7.0.25:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    def configure_args(self):
        args = []
        ldflags = []
        libs = []
        for lib in ["libpng", "bzip2"]:
            if self.spec[lib].satisfies("+shared") or self.spec[lib].satisfies("libs=shared"):
                continue
            ldflags.append(self.spec[lib].libs.ld_flags)
            libs.append(self.spec[lib].libs.link_flags)
        if ldflags:
            args.append("LDFLAGS=%s" % " ".join(ldflags))
            args.append("LIBS=%s" % " ".join(libs))
        return args
