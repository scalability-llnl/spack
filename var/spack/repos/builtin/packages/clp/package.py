# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Clp(AutotoolsPackage):
    """Clp (Coin-or linear programming) is an open-source
    linear programming solver written in C++."""

    homepage = "https://projects.coin-or.org/Clp"
    url = "https://github.com/coin-or/Clp/archive/releases/1.17.6.tar.gz"

    license("EPL-2.0")

    version("1.17.9", sha256="b02109be54e2c9c6babc9480c242b2c3c7499368cfca8c0430f74782a694a49f")
    version("1.17.7", sha256="c4c2c0e014220ce8b6294f3be0f3a595a37bef58a14bf9bac406016e9e73b0f5")
    version("1.17.6", sha256="afff465b1620cfcbb7b7c17b5d331d412039650ff471c4160c7eb24ae01284c9")
    version("1.17.4", sha256="ef412cde00cb1313d9041115a700d8d59d4b8b8b5e4dde43e9deb5108fcfbea8")
    version("1.16.11", sha256="b525451423a9a09a043e6a13d9436e13e3ee7a7049f558ad41a110742fa65f39")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("coinutils")
    depends_on("osi")
    depends_on("pkgconfig", type="build")

    build_directory = "spack-build"
