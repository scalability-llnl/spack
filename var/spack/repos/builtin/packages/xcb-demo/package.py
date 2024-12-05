# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbDemo(AutotoolsPackage):
    """xcb-demo: A collection of demo programs that use the XCB library."""

    homepage = "https://xcb.freedesktop.org/"
    url = "https://xcb.freedesktop.org/dist/xcb-demo-0.1.tar.gz"

    version("0.1", sha256="19ace2812a05313747356dc5e2331a9a6f5eb46631a26819cf30eeeaa38077f9")

    depends_on("c", type="build")  # generated

    depends_on("libxcb")
    depends_on("xcb-util")
    depends_on("xcb-util-image")
    depends_on("xcb-util-wm")

    depends_on("pkgconfig", type="build")

    # FIXME: crashes with the following error message
    # X11/XCB/xcb.h: No such file or directory
