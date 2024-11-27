# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Editres(AutotoolsPackage, XorgPackage):
    """Dynamic resource editor for X Toolkit applications."""

    homepage = "https://cgit.freedesktop.org/xorg/app/editres"
    xorg_mirror_path = "app/editres-1.0.6.tar.gz"

    version("1.0.8", sha256="2d56d6077bc767afa7e030feb2c372fe6be893fec4029a23f45a1d559fd846ae")
    version("1.0.6", sha256="85f4664ca582effb01ee972d006124569b757b9a08ae6608c3f45fc36b3b7b1a")

    depends_on("c", type="build")  # generated

    depends_on("libxaw")
    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxmu")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
