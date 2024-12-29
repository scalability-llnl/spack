# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxpresent(AutotoolsPackage, XorgPackage):
    """This package contains header files and documentation for the Present
    extension.  Library and server implementations are separate."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXpresent/"
    xorg_mirror_path = "lib/libXpresent-1.0.0.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.0.1", sha256="8ebf8567a8f6afe5a64275a2ecfd4c84e957970c27299d964350f60be9f3541d")
    version("1.0.0", sha256="92f1bdfb67ae2ffcdb25ad72c02cac5e4912dc9bc792858240df1d7f105946fa")

    depends_on("c", type="build")

    depends_on("libx11", type="link")
    depends_on("libxext", type="link")
    depends_on("libxfixes", type="link")
    depends_on("libxrandr", type="link")

    depends_on("xproto", type=("build", "link"))
    depends_on("presentproto@1.0:", type=("build", "link"))
    depends_on("xextproto", type="build")
    depends_on("fixesproto", type="build")
    depends_on("randrproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
