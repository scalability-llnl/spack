# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Appres(AutotoolsPackage, XorgPackage):
    """The appres program prints the resources seen by an application (or
    subhierarchy of an application) with the specified class and instance
    names.  It can be used to determine which resources a particular
    program will load."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/appres"
    xorg_mirror_path = "app/appres-1.0.4.tar.gz"

    version("1.0.6", sha256="848f383ff429612fb9df840d79e97dc193dc72dbbf53d3217a8d1e90a5aa1e26")
    version("1.0.4", sha256="22cb6f639c891ffdbb5371bc50a88278185789eae6907d05e9e0bd1086a80803")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxt")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
