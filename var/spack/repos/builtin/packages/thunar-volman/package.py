# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class ThunarVolman(AutotoolsPackage):
    """Thunar extension  which enables automatic management of removable drives and media."""

    homepage = "https://docs.xfce.org/xfce/thunar/thunar-volman"
    url = "https://archive.xfce.org/xfce/4.18/src/thunar-volman-4.18.0.tar.bz2"

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("4.18.0", sha256="93b75c7ffbe246a21f4190295acc148e184be8df397e431b258d0d676e87fc65")

    extends("thunar")

    # Base requirements
    depends_on("intltool@0.39.0:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4util")
        depends_on("xfconf")
        depends_on("libxfce4ui")
        depends_on("exo")
        depends_on("libgudev")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")
        depends_on("dbus-glib")
        with when("@4.18.0:"):
            depends_on("glib@2.66:")
            depends_on("gtkplus@3.24:")
            depends_on("libgudev@145:")
