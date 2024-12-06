# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Presentproto(AutotoolsPackage, XorgPackage):
    """Present protocol specification and Xlib/Xserver headers."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/presentproto/"
    xorg_mirror_path = "proto/presentproto-1.0.tar.gz"

    version("1.1", sha256="114252e97afb4dfae8b31e6b0d5e24e4babda26b364e2be57abc2f3c30248b87")
    version("1.0", sha256="02f8042cb351dd5c3699a0dbdb2ab25f86532efe3e1e3e97897e7f44b5c67040")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
