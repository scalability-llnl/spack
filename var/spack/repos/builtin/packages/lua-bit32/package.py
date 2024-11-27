# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LuaBit32(LuaPackage):
    """Lua 5.2 bit operations for Lua 5.1"""

    homepage = "https://luarocks.org/modules/siffiejoe/bit32/"
    url = "https://luarocks.org/manifests/siffiejoe/bit32-5.3.5.1-1.src.rock"

    license("MIT")

    version(
        "5.3.5.1-1",
        sha256="0e273427f2b877270f9cec5642ebe2670242926ba9638d4e6df7e4e1263ca12c",
        expand=False,
    )

    depends_on("lua-lang@5.1")
