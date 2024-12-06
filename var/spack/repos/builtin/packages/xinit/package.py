# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xinit(AutotoolsPackage, XorgPackage):
    """The xinit program is used to start the X Window System server and a
    first client program on systems that are not using a display manager
    such as xdm."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xinit"
    xorg_mirror_path = "app/xinit-1.3.4.tar.gz"

    license("MIT")

    version("1.4.2", sha256="9121c9162f6dedab1229a8c4ed4021c4d605699cb0da580ac2ee1b0c96b3f60e")
    version("1.4.1", sha256="ca33ec3de6c39589c753620e5b3bcbc8277218b949bfa2df727779b03a8d2357")
    version("1.4.0", sha256="17548a5df41621b87d395f1074dfb88b0dc6917f9127540b89c6de4a80f33776")
    version("1.3.4", sha256="754c284875defa588951c1d3d2b20897d3b84918d0a97cb5a4724b00c0da0746")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libx11")

    depends_on("xproto@7.0.17:")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
