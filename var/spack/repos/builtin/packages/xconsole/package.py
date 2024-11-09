# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xconsole(AutotoolsPackage, XorgPackage):
    """xconsole displays in a X11 window the messages which are usually sent
    to /dev/console."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xconsole"
    xorg_mirror_path = "app/xconsole-1.0.6.tar.gz"

    version("1.1.0", sha256="fe5d2ba99b754909b2a04ce4abf054cd1e3134a830d69aea82e8465cc9f73942")
    version("1.0.8", sha256="1897be35738489f92ef511caef189db8d5079469374021dc09b59e89992b7c29")
    version("1.0.7", sha256="91bc7327643b1ca57800a37575930af16fbea485d426a96d8f465de570aa6eb3")
    version("1.0.6", sha256="28151453a0a687462516de133bac0287b488a2ff56da78331fee34bc1bf3e7d5")

    depends_on("c", type="build")

    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libxt@1.0:")
    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
