# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbUtil(AutotoolsPackage, XorgPackage):
    """The XCB util modules provides a number of libraries which sit on top
    of libxcb, the core X protocol library, and some of the extension
    libraries. These experimental libraries provide convenience functions
    and interfaces which make the raw X protocol more usable. Some of the
    libraries also provide client-side code which is not strictly part of
    the X protocol but which have traditionally been provided by Xlib."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxcb-util"
    xorg_mirror_path = "lib/xcb-util-0.4.1.tar.xz"

    license("MIT")

    version("0.4.1", sha256="5abe3bbbd8e54f0fa3ec945291b7e8fa8cfd3cccc43718f8758430f94126e512")
    version(
        "0.4.0",
        sha256="0ed0934e2ef4ddff53fcc70fc64fb16fe766cd41ee00330312e20a985fd927a7",
        url="https://xcb.freedesktop.org/dist/xcb-util-0.4.0.tar.gz",
    )

    depends_on("c", type="build")  # generated

    depends_on("libxcb@1.4:")

    depends_on("pkgconfig", type="build")
