# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libgudev(MesonPackage):
    """Provides GObject bindings for libudev."""

    homepage = "https://gitlab.gnome.org/GNOME/libgudev/"
    url = "https://download.gnome.org/sources/libgudev/238/libgudev-238.tar.xz"

    maintainers("teaguesterling")

    license("LGPL2.1", checked_by="teaguesterling")

    version("238", sha256="61266ab1afc9d73dbc60a8b2af73e99d2fdff47d99544d085760e4fa667b5dd1")

    with default_args(type=("build", "link", "run")):
        depends_on("glib@2.38:")
        depends_on("systemd@251:")  # For libuvdev
