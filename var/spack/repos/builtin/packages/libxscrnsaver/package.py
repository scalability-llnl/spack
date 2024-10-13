# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxscrnsaver(AutotoolsPackage, XorgPackage):
    """XScreenSaver - X11 Screen Saver extension client library"""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXScrnSaver"
    xorg_mirror_path = "lib/libXScrnSaver-1.2.2.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.2.4", sha256="0656b2630475104d6df75d91ebb8e0153e61d14e9871ef1f403bcda4a62a838a")
    version("1.2.3", sha256="4f74e7e412144591d8e0616db27f433cfc9f45aae6669c6c4bb03e6bf9be809a")
    version("1.2.2", sha256="e12ba814d44f7b58534c0d8521e2d4574f7bf2787da405de4341c3b9f4cc8d96")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext")

    depends_on("xextproto", type="build")
    depends_on("scrnsaverproto@1.2:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
