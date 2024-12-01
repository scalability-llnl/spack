# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xf86dga(AutotoolsPackage, XorgPackage):
    """dga is a simple test client for the XFree86-DGA extension."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xf86dga"
    xorg_mirror_path = "app/xf86dga-1.0.3.tar.gz"

    version("1.0.3", sha256="acbf89f60a99b18c161d2beb0e4145a0fdf6c516f7f45fa52e547d88491f75c9")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxxf86dga@1.1:")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
