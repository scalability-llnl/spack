# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbUtilImage(AutotoolsPackage, XorgPackage):
    """The XCB util modules provides a number of libraries which sit on top
    of libxcb, the core X protocol library, and some of the extension
    libraries. These experimental libraries provide convenience functions
    and interfaces which make the raw X protocol more usable. Some of the
    libraries also provide client-side code which is not strictly part of
    the X protocol but which have traditionally been provided by Xlib."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxcb-image"
    xorg_mirror_path = "lib/xcb-util-image-0.4.1.tar.xz"

    license("MIT")

    version("0.4.1", sha256="ccad8ee5dadb1271fd4727ad14d9bd77a64e505608766c4e98267d9aede40d3d")
    version(
        "0.4.0",
        sha256="cb2c86190cf6216260b7357a57d9100811bb6f78c24576a3a5bfef6ad3740a42",
        url="https://xcb.freedesktop.org/dist/xcb-util-image-0.4.0.tar.gz",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("libxcb@1.4:")
    depends_on("xcb-util")

    depends_on("xproto@7.0.8:")
    depends_on("pkgconfig", type="build")
