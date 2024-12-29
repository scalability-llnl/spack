# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfce4Appfinder(AutotoolsPackage):
    """Program to find and launch installed applications for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/xfce4-appfinder/start"
    url = "https://archive.xfce.org/xfce/4.16/src/xfce4-appfinder-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="962a98d7b327d2073ed4cd0f78bce7945ed51b97d52fd60196e8b02ef819c18c")
    version("4.16.0", sha256="37b92aaaeeec8220ed23163cf89321168d3b49e0c48b4c10f12dc4a21fdf0954")

    # Base requirements
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4ui")
        depends_on("garcon")
        depends_on("glib@2:")

    depends_on("intltool@0.35.0:", type="build")
    with default_args(type=("build", "link", "run")):
        with when("@4.18.0:"):
            depends_on("glib@2.66:")
        with when("@4.16.0:"):
            depends_on("glib@2.50:")
