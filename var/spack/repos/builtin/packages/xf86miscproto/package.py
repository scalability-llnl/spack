# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xf86miscproto(AutotoolsPackage, XorgPackage):
    """This package includes the protocol definitions of the "XFree86-Misc"
    extension to the X11 protocol.  The "XFree86-Misc" extension is
    supported by the XFree86 X server and versions of the Xorg X server
    prior to Xorg 1.6."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xf86miscproto"
    xorg_mirror_path = "proto/xf86miscproto-0.9.3.tar.gz"

    version("0.9.3", sha256="1b05cb76ac165c703b82bdd270b86ebbc4d42a7d04d299050b07ba2099c31352")
