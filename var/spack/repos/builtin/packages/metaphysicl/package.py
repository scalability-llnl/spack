# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Metaphysicl(AutotoolsPackage):
    """Metaprogramming and operator-overloaded classes for
    numerical simulations."""

    homepage = "https://github.com/roystgnr/MetaPhysicL"
    url = "https://github.com/roystgnr/MetaPhysicL/archive/v0.2.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.6.0", sha256="a1b8469de17ad9960b4c99a9dbe2db46b7da50f97c811467efce470585d3f7f2")
    version("0.5.0", sha256="dbba0590970a128ae2ae7064b621f78f95ca2303b70a12b079a51702573840a6")
    version("0.3.3", sha256="6581ec6512d3509bfca6f93052f7d47dd2d9e4b9f2b3580d778495ae381a0b0d")
    version("0.2.0", sha256="ff4f9fad870dcdc85d56fb1f8d94123fecbef9189f967d254ba9607624b5f32e")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
