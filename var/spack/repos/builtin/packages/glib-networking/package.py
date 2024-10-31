# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlibNetworking(MesonPackage):
    """Network-related giomodules for glib."""

    homepage = "https://gitlab.gnome.org/GNOME/glib-networking"
    url = "https://github.com/GNOME/glib-networking/archive/2.66.0.tar.gz"

    license("LGPL-2.0-or-later")

    version("2.66.0", sha256="186a670c00525d62aa160bc3e492d9efd2f59c540c50477982eb732ed62ee96c")
    version("2.65.90", sha256="91b35c5d7472d10229b0b01c0631ac171903e96f84a6fb22c4126a40528c09e2")
    version("2.65.1", sha256="d06311004f7dda4561c210f286a3678b631fb7187cb3b90616c5ba39307cc91f")

    depends_on("c", type="build")

    depends_on("gettext", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("glib")
    depends_on("gnutls")
    depends_on("gsettings-desktop-schemas")
    depends_on("libproxy")
