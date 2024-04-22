# Copyright 2013-2023 Lawrence Livermore National Security, LLC and otherargs
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Mplayer(AutotoolsPackage):
    """Mplayer is a movie player for linux"""

    # DJV: I'm guessing there is a lot more we can do to add in more packages
    # and codecs but this is working for now and gets us a GUI

    homepage = "http://www.mplayerhq.hu"
    url = "https://mplayerhq.hu/MPlayer/releases/MPlayer-1.5.tar.xz"

    version("1.5", sha256="650cd55bb3cb44c9b39ce36dac488428559799c5f18d16d98edb2b7256cbbf85")

    variant("gui", default=True, description="GUI support")

    depends_on("pkgconfig", type="build")
    depends_on("yasm")
    depends_on("gtkplus", when="+gui")

    def configure_args(self):
        spec = self.spec
        args = [
            f"--yasm={spec['yasm'].prefix.bin.yasm}",
        ]

        if "+gui" in self.spec:
            args.append("--enable-gui")

        return args
