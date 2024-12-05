# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ecdsautils(CMakePackage):
    """Tiny collection of programs used for ECDSA."""

    homepage = "https://github.com/freifunk-gluon/ecdsautils/"
    url = "https://github.com/freifunk-gluon/ecdsautils/archive/refs/tags/v0.3.2.tar.gz"

    license("BSD-2-Clause AND MIT", checked_by="wdconinc")

    version("0.4.1", sha256="6fd827b3070afddc9e31f37f1d805f54aabf8518d2310c5c2b26cc8eb53555a8")
    version("0.3.2", sha256="a828417c985ccfc623bb613e92ccc8af6c6f24a5bcab8b112b90c033a816204f")
    version("0.3.1", sha256="4b6efe7802a089e8d64194c954a8f9981ff516b922b40d51e6c7ba565274a87a")

    depends_on("c", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libuecc@3:")
    depends_on("libuecc@6:", when="@0.4:")
