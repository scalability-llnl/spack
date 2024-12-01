# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Videoproto(AutotoolsPackage, XorgPackage):
    """X Video Extension.

    This extension provides a protocol for a video output mechanism,
    mainly to rescale video playback in the video controller hardware."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/videoproto"
    xorg_mirror_path = "proto/videoproto-2.3.3.tar.gz"

    version("2.3.3", sha256="df8dfeb158767f843054248d020e291a2c40f7f5e0ac6d8706966686fee7c5c0")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
