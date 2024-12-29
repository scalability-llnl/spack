# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libice(AutotoolsPackage, XorgPackage):
    """libICE - Inter-Client Exchange Library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libICE"
    xorg_mirror_path = "lib/libICE-1.0.9.tar.gz"

    license("X11")

    maintainers("wdconinc")

    version("1.1.1", sha256="04fbd34a11ba08b9df2e3cdb2055c2e3c1c51b3257f683d7fcf42dabcf8e1210")
    version("1.1.0", sha256="7a735ec530d7a437955747eabac06bbc0b695da77fd1b4d1df3b0a483d823875")
    version("1.0.10", sha256="1116bc64c772fd127a0d0c0ffa2833479905e3d3d8197740b3abd5f292f22d2d")
    version("1.0.9", sha256="7812a824a66dd654c830d21982749b3b563d9c2dfe0b88b203cefc14a891edc0")

    depends_on("c", type="build")

    # technically libbsd is only required when glibc < 2.36 which provides arc4random_buf,
    # but spack doesn't currently have a good way to model this so we depend on it unconditionally
    depends_on("libbsd", when="platform=linux")

    depends_on("xproto", type=("build", "link"))
    depends_on("xtrans")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    @property
    def libs(self):
        return find_libraries("libICE", self.prefix, shared=True, recursive=True)
