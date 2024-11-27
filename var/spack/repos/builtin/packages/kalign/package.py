# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kalign(AutotoolsPackage, CMakePackage):
    """A fast multiple sequence alignment program for biological sequences."""

    homepage = "https://github.com/TimoLassmann/kalign"
    url = "https://github.com/TimoLassmann/kalign/archive/refs/tags/v3.3.1.tar.gz"

    license("GPL-3.0-or-later")

    version("3.4.0", sha256="67d1a562d54b3b7622cc3164588c05b9e2bf8f1a5140bb48a4e816c61a87d4a8")
    version("3.3.1", sha256="7f10acf9a3fa15deabbc0304e7c14efa25cea39108318c9f02b47257de2d7390")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_system(
        conditional("cmake", when="@3.4.0:"),
        conditional("autotools", when="@3.3.1"),
        default="cmake",
    )

    with when("build_system=cmake"):
        depends_on("cmake@3.18:", type="build")

    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
