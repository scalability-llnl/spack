# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xterm(AutotoolsPackage):
    """The xterm program is a terminal emulator for the X Window System. It
    provides DEC VT102 and Tektronix 4014 compatible terminals for programs
    that can't use the window system directly."""

    homepage = "https://invisible-island.net/xterm/"
    url = "https://invisible-island.net/archives/xterm/xterm-327.tgz"

    license("MIT")

    version("393", sha256="dc3abf533d66ae3db49e6783b0e1e29f0e4d045b4b3dac797a5e93be2735ec7b")
    version("353", sha256="e521d3ee9def61f5d5c911afc74dd5c3a56ce147c7071c74023ea24cac9bb768")
    version("350", sha256="aefb59eefd310268080d1a90a447368fb97a9a6737bfecfc3800bf6cc304104d")
    version("340", sha256="b5c7f77b7afade798461e2a2f86d5af64f9c9c9f408b1af0f545add978df722a")
    version("330", sha256="7aeef9f29f6b95e09f481173c8c3053357bf5ffe162585647f690fd1707556df")
    version("327", sha256="66fb2f6c35b342148f549c276b12a3aa3fb408e27ab6360ddec513e14376150b")

    depends_on("libxft")
    depends_on("fontconfig")
    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libxt")
    depends_on("libx11")
    depends_on("libxinerama")
    depends_on("libxpm")
    depends_on("libice")
    depends_on("freetype")
    depends_on("libxrender")
    depends_on("libxext")
    depends_on("libsm")
    depends_on("libxcb")
    depends_on("libxau")
    depends_on("bzip2")

    depends_on("pkgconfig", type="build")
    depends_on("termcap", type="link")
