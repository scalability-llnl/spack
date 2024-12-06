# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Orbit2(AutotoolsPackage):
    """ORBit is a fast and lightweight CORBA server."""

    homepage = "https://developer.gnome.org"
    url = "https://ftp.gnome.org/pub/GNOME/sources/ORBit2/2.14/ORBit2-2.14.19.tar.bz2"

    license("LGPL-2.0-only")

    version("2.14.19", sha256="55c900a905482992730f575f3eef34d50bda717c197c97c08fa5a6eafd857550")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("glib")
    depends_on("libidl")
