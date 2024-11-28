# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Beforelight(AutotoolsPackage, XorgPackage):
    """The beforelight program is a sample implementation of a screen saver
    for X servers supporting the MIT-SCREEN-SAVER extension.   It is only
    recommended for use as a code sample, as it does not include features
    such as screen locking or configurability."""

    homepage = "https://cgit.freedesktop.org/xorg/app/beforelight"
    xorg_mirror_path = "app/beforelight-1.0.5.tar.gz"

    license("X11")

    version("1.0.6", sha256="735579a7671a9f9de16b7211cf0ba39027183bdc3e82a937fbccfdd893e64a2e")
    version("1.0.5", sha256="93bb3c457d6d5e8def3180fdee07bc84d1b7f0e5378a95812e2193cd51455cdc")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxscrnsaver")
    depends_on("libxt")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
