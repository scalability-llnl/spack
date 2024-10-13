# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libxcvt(MesonPackage, XorgPackage):
    """Implementation of the VESA CVT standard timing modelines generator."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxcvt"
    xorg_mirror_path = "lib/libxcvt-0.1.2.tar.xz"

    license("MIT", checked_by="teaguesterling")

    version("0.1.2", sha256="0561690544796e25cfbd71806ba1b0d797ffe464e9796411123e79450f71db38")
