# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xdpyinfo(AutotoolsPackage, XorgPackage):
    """xdpyinfo is a utility for displaying information about an X server.

    It is used to examine the capabilities of a server, the predefined
    values for various parameters used in communicating between clients
    and the server, and the different types of screens, visuals, and X11
    protocol extensions that are available."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xdpyinfo"
    xorg_mirror_path = "app/xdpyinfo-1.3.2.tar.gz"

    license("custom")

    version("1.3.3", sha256="2ae7b8213ea839b8376843477496276e8d69550c48bff081e16376539fc27c5a")
    version("1.3.2", sha256="ef39935e8e9b328e54a85d6218d410d6939482da6058db1ee1b39749d98cbcf2")

    depends_on("c", type="build")

    depends_on("libxext")
    depends_on("libx11")
    depends_on("libxtst")
    depends_on("libxcb")

    depends_on("xproto@7.0.22:", type="build")
    depends_on("recordproto", type="build")
    depends_on("inputproto", type="build")
    depends_on("fixesproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
