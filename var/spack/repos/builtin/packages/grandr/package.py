# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grandr(AutotoolsPackage, XorgPackage):
    """RandR user interface using GTK+ libraries."""

    homepage = "https://cgit.freedesktop.org/xorg/app/grandr"
    xorg_mirror_path = "app/grandr-0.1.tar.gz"

    version("0.1", sha256="67a049c8dccdb48897efbd86c2b1d3b0ff5ce3c7859c46b0297d64c881b36d24")

    depends_on("c", type="build")  # generated

    depends_on("gtkplus@2.0.0:")
    depends_on("gconf")
    depends_on("xrandr@1.2:")
