# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xsm(AutotoolsPackage, XorgPackage):
    """X Session Manager."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xsm"
    xorg_mirror_path = "app/xsm-1.0.3.tar.gz"

    version("1.0.5", sha256="e8a2f64b5a37be39a81877cd4069745a226a31493080f03ae74b76fb3f17b7a6")
    version("1.0.4", sha256="d12fb0071719de5845d41602963988e4b889f482427c13ce8e515f5ca51c0564")
    version("1.0.3", sha256="f70815139d62416dbec5915ec37db66f325932a69f6350bb1a74c0940cdc796a")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxt@1.1.0:")
    depends_on("libice")
    depends_on("libsm")
    depends_on("libxaw")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
