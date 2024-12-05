# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbUtilRenderutil(AutotoolsPackage, XorgPackage):
    """The XCB util modules provides a number of libraries which sit on top
    of libxcb, the core X protocol library, and some of the extension
    libraries. These experimental libraries provide convenience functions
    and interfaces which make the raw X protocol more usable. Some of the
    libraries also provide client-side code which is not strictly part of
    the X protocol but which have traditionally been provided by Xlib."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxcb-renderutil"
    xorg_mirror_path = "lib/xcb-util-renderutil-0.3.10.tar.xz"

    license("MIT")

    version("0.3.10", sha256="3e15d4f0e22d8ddbfbb9f5d77db43eacd7a304029bf25a6166cc63caa96d04ba")
    version(
        "0.3.9",
        sha256="55eee797e3214fe39d0f3f4d9448cc53cffe06706d108824ea37bb79fcedcad5",
        url="https://xcb.freedesktop.org/dist/xcb-util-renderutil-0.3.9.tar.gz",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("libxcb@1.4:")

    depends_on("pkgconfig", type="build")
