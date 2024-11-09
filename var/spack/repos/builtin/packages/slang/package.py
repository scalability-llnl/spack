# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Slang(AutotoolsPackage):
    """An interpreted language and programing library."""

    homepage = "https://www.jedsoft.org/slang"
    url = "https://www.jedsoft.org/releases/slang/slang-2.3.2.tar.bz2"

    license("GPL-2.0-or-later")

    version("2.3.3", sha256="f9145054ae131973c61208ea82486d5dd10e3c5cdad23b7c4a0617743c8f5a18")
    version("2.3.2", sha256="fc9e3b0fc4f67c3c1f6d43c90c16a5c42d117b8e28457c5b46831b8b5d3ae31a")
    version("2.3.1", sha256="a810d5da7b0c0c8c335393c6b4f12884be6fa7696d9ca9521ef21316a4e00f9d")

    depends_on("c", type="build")  # generated

    parallel = False
