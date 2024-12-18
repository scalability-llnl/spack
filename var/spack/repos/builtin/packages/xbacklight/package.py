# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xbacklight(AutotoolsPackage, XorgPackage):
    """Xbacklight is used to adjust the backlight brightness where supported.
    It uses the RandR extension to find all outputs on the X server
    supporting backlight brightness control and changes them all in the
    same way."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xbacklight"
    xorg_mirror_path = "app/xbacklight-1.2.1.tar.gz"

    license("MIT")

    version("1.2.3", sha256="d2a8dd962454d8de3675286eab4edc4d1376ac7da040a3a8729ee250e6e798c1")
    version("1.2.2", sha256="9812497b95b28776539808ba75e8b8a2d48a57416e172e04e9580e65c76a61bb")
    version("1.2.1", sha256="82c80cd851e3eb6d7a216d92465fcf6d5e456c2d5ac12c63cd2757b39fb65b10")

    depends_on("c", type="build")  # generated

    depends_on("libxcb")
    depends_on("xcb-util")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
