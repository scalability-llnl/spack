# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gconf(AutotoolsPackage):
    """GConf is a system for storing application preferences.

    Note that this software is now deprecated in favor of moving to GSettings
    and dconf with the GNOME 3 transition.
    """

    homepage = "https://en.wikipedia.org/wiki/GConf"
    url = "http://ftp.gnome.org/pub/gnome/sources/GConf/3.2/GConf-3.2.6.tar.xz"

    version(
        "3.2.6",
        sha256="1912b91803ab09a5eed34d364bf09fe3a2a9c96751fde03a4e0cfa51a04d784c",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("gettext", type="build")
    depends_on("intltool", type="build")
    depends_on("glib@2.14.0:")
    depends_on("libxml2")
    depends_on("dbus")
    depends_on("dbus-glib")
    depends_on("orbit2")
    depends_on("perl-xml-parser", type=("build", "run"))
