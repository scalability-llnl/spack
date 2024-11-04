# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SblimSfcc(AutotoolsPackage):
    """Small Footprint CIM Client Library"""

    homepage = "https://sourceforge.net/projects/sblim/"
    url = "https://github.com/kkaempf/sblim-sfcc/archive/SFCC_2_2_1.tar.gz"

    license("EPL-1.0")

    version("2_2_8", sha256="d8d0bf06a487483df507f512ddf0c7b2c1b878a1c9b039bf5c2357c4ba13b882")
    version("2_2_7", sha256="bb85bc75efd112411eb76e83a38413a33b3fb8b6b725c8d08fe326efcbea427f")
    version("2_2_6", sha256="65a8b70047c449f8b60e519ec1a47aa50b6476d3876a698e8484467650e9ee78")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("curl")
