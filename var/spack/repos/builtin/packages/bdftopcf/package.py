# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bdftopcf(AutotoolsPackage, XorgPackage):
    """bdftopcf is a font compiler for the X server and font server.  Fonts
    in Portable Compiled Format can be read by any architecture, although
    the file is structured to allow one particular architecture to read
    them directly without reformatting.  This allows fast reading on the
    appropriate machine, but the files are still portable (but read more
    slowly) on other machines."""

    homepage = "https://gitlab.freedesktop.org/xorg/util/bdftopcf"
    xorg_mirror_path = "util/bdftopcf-1.0.5.tar.gz"

    license("MIT")

    version("1.1.1", sha256="3291df9910c006a0345f3eac485e2a5734bbb79a0d97bf1f2b4cddad48fb1bc4")
    version("1.1", sha256="699d1a62012035b1461c7f8e3f05a51c8bd6f28f348983249fb89bbff7309b47")
    version("1.0.5", sha256="78a5ec945de1d33e6812167b1383554fda36e38576849e74a9039dc7364ff2c3")

    # note: url_for_version can only return a single url, no mirrors
    @when("@:1.1.0")
    def url_for_version(self, version):
        return self.urls[0].replace("util", "app")

    depends_on("c", type="build")

    depends_on("libxfont")

    depends_on("pkgconfig", type="build")
    depends_on("xproto", type="build")
    depends_on("fontsproto", type="build")
    depends_on("util-macros", type="build")
