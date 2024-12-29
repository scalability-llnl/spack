# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfconf(AutotoolsPackage):
    """xfconf - Configuration Storage System for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/xfconf/start"
    url = "https://archive.xfce.org/xfce/4.16/src/xfconf-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")

    license("LGPLv2.1", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="2e8c50160bf800a807aea094fc9dad81f9f361f42db56607508ed5b4855d2906")
    version("4.16.0", sha256="652a119007c67d9ba6c0bc7a740c923d33f32d03dc76dfc7ba682584e72a5425")

    depends_on("intltool@0.35.0:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4util")
        depends_on("dbus-glib")
        with when("@4.18"):
            depends_on("glib@2.66:")
            depends_on("gettext")  # Undocumented
        with when("@4.16"):
            depends_on("glib@2.50:")
