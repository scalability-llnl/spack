# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xrx(AutotoolsPackage, XorgPackage):
    """The remote execution (RX) service specifies a MIME format for invoking
    applications remotely, for example via a World Wide Web browser.  This
    RX format specifies a syntax for listing network services required by
    the application, for example an X display server.  The requesting Web
    browser must identify specific instances of the services in the request
    to invoke the application."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xrx"
    xorg_mirror_path = "app/xrx-1.0.4.tar.gz"

    version("1.0.4", sha256="1ffa1c2af28587c6ed7ded3af2e62e93bad8f9900423d09c45b1d59449d15134")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxext")
    depends_on("libxau")
    depends_on("libice")
    depends_on("libxaw")

    depends_on("xtrans")
    depends_on("xproxymanagementprotocol", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
