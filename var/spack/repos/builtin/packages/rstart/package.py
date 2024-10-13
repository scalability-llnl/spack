# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rstart(AutotoolsPackage, XorgPackage):
    """This package includes both the client and server sides implementing
    the protocol described in the "A Flexible Remote Execution Protocol
    Based on rsh" paper found in the specs/ subdirectory.

    This software has been deprecated in favor of the X11 forwarding
    provided in common ssh implementations."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/rstart"
    xorg_mirror_path = "app/rstart-1.0.5.tar.gz"

    version("1.0.6", sha256="28aa687437efeee70965a0878f9db79397cf691f4011268e16bc835627e23ec5")
    version("1.0.5", sha256="5271c0c2675b4ad09aace7edddfdd137af10fc754afa6260d8eb5d0bba7098c7")

    depends_on("c", type="build")

    depends_on("xproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
