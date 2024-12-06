# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scripts(AutotoolsPackage, XorgPackage):
    """Various X related scripts."""

    homepage = "https://cgit.freedesktop.org/xorg/app/scripts"
    xorg_mirror_path = "app/scripts-1.0.1.tar.gz"

    version("1.0.1", sha256="0ed6dabdbe821944d61830489ad5f21bd934550456b9157a1cd8a32f76e08279")

    depends_on("cxx", type="build")  # generated

    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
