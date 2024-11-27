# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Windowswmproto(AutotoolsPackage, XorgPackage):
    """This module provides the definition of the WindowsWM extension to the
    X11 protocol, used for coordination between an X11 server and the
    Microsoft Windows native window manager.

    WindowsWM is only intended to be used on Cygwin when running a
    rootless XWin server."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/windowswmproto"
    xorg_mirror_path = "proto/windowswmproto-1.0.4.tar.gz"

    version("1.0.4", sha256="2dccf510cf18a1b5cfd3a277c678d88303efc85478b479fec46228a861956eb7")
