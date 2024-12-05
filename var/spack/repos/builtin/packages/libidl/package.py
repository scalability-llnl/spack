# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libidl(AutotoolsPackage):
    """libraries for Interface Definition Language files"""

    homepage = "https://developer.gnome.org/"
    url = "https://ftp.gnome.org/pub/gnome/sources/libIDL/0.8/libIDL-0.8.14.tar.bz2"

    license("LGPL-2.0-or-later")

    version("0.8.14", sha256="c5d24d8c096546353fbc7cedf208392d5a02afe9d56ebcc1cccb258d7c4d2220")

    depends_on("c", type="build")  # generated

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("glib")
