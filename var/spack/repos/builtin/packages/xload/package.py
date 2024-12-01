# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xload(AutotoolsPackage, XorgPackage):
    """xload displays a periodically updating histogram of the
    system load average."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xload"
    xorg_mirror_path = "app/xload-1.1.3.tar.gz"

    license("MIT")

    version("1.2.0", sha256="0d3b84d22d2d85e9c3c152e48871e490dfcaad420f8836333f1323c5a690d55f")
    version("1.1.4", sha256="4e3d240ab63e02f2ddac8182519d94bea82bda4887e3e364dd8832a04ca8436a")
    version("1.1.3", sha256="9952e841d25ab2fd0ce5e27ba91858331c3f97575d726481772d4deb89432483")
    version("1.1.2", sha256="4863ad339d22c41a0ca030dc5886404f5ae8b8c47cd5e09f0e36407edbdbe769")

    depends_on("c", type="build")

    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libxt")
    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    def configure_args(self):
        return ["ac_cv_search_gettext=no"]
