# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xbitmaps(AutotoolsPackage, XorgPackage):
    """The xbitmaps package contains bitmap images used by multiple
    applications built in Xorg."""

    homepage = "https://gitlab.freedesktop.org/xorg/data/bitmaps/"
    xorg_mirror_path = "data/xbitmaps-1.1.1.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.1.3", sha256="93b433b7ff223c4685fdba583b4bd30f2706be2413a670021084422d85b0269d")
    version("1.1.2", sha256="27e700e8ee02c43f7206f4eca8f1953ad15236cac95d7a0f08505c3f7d99c265")
    version("1.1.1", sha256="3bc89e05be4179ce4d3dbba1ae554da4591d41f7a489d9e2735a18cfd8378188")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
