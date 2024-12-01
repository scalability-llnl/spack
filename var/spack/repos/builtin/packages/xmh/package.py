# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xmh(AutotoolsPackage, XorgPackage):
    """The xmh program provides a graphical user interface to the
    MH Message Handling System.  To actually do things with your
    mail, it makes calls to the MH package."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xmh"
    xorg_mirror_path = "app/xmh-1.0.3.tar.gz"

    version("1.0.5", sha256="3ab74096031ba89bcc88a46dbfa652837c4aeb6a36168ff9799782efe88128b8")
    version("1.0.4", sha256="2034f24fb3181b6e07ebf7235d2845a7ebb18d533aa405dbc99235eec4ab410f")
    version("1.0.3", sha256="f90baf2615a4e1e01232c50cfd36ee4d50ad2fb2f76b8b5831fb796661f194d2")

    depends_on("c", type="build")  # generated

    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libxt")
    depends_on("libx11")

    depends_on("xbitmaps@1.1.0:")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
