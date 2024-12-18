# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LuaFfi(LuaPackage):
    """luajit FFI for interpreted lua"""

    homepage = "https://github.com/facebook/luaffifb/"
    git = "https://github.com/facebook/luaffifb/"
    url = "https://github.com/facebook/luaffifb/"

    maintainers("trws")

    license("BSD-3-Clause")

    version(
        "0.0.1.fakever",
        git="https://github.com/facebook/luaffifb/",
        commit="a1cb731b08c91643b0665935eb5622b3d621211b",
    )

    depends_on("c", type="build")  # generated

    depends_on("lua-lang@5.1")
