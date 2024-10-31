# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xcmsdb(AutotoolsPackage, XorgPackage):
    """xcmsdb is used to load, query, or remove Device Color Characterization
    data stored in properties on the root window of the screen as
    specified in section 7, Device Color Characterization, of the
    X11 Inter-Client Communication Conventions Manual (ICCCM)."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xcmsdb"
    xorg_mirror_path = "app/xcmsdb-1.0.5.tar.gz"

    license("custom")

    version("1.0.6", sha256="640b42c746eb34bdd71ca2850f2bc9fb0ade194c9f152a8d002425a0684df077")
    version("1.0.5", sha256="8442352ee5eb3ea0d3a489c26d734e784ef6964150c2a173401d0dc6638ca236")

    depends_on("c", type="build")  # generated

    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
