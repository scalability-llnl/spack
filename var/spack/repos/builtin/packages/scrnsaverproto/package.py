# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scrnsaverproto(AutotoolsPackage, XorgPackage):
    """MIT Screen Saver Extension.

    This extension defines a protocol to control screensaver features
    and also to query screensaver info on specific windows."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/scrnsaverproto"
    xorg_mirror_path = "proto/scrnsaverproto-1.2.2.tar.gz"

    license("X11")

    version("1.2.2", sha256="d8dee19c52977f65af08fad6aa237bacee11bc5a33e1b9b064e8ac1fd99d6e79")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
