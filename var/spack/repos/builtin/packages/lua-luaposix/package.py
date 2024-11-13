# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LuaLuaposix(LuaPackage):
    """Lua posix bindings, including ncurses"""

    homepage = "https://github.com/luaposix/luaposix/"
    url = "https://github.com/luaposix/luaposix/archive/release-v33.4.0.tar.gz"

    license("MIT")

    version(
        "35.0",
        sha256="a4edf2f715feff65acb009e8d1689e57ec665eb79bc36a6649fae55eafd56809",
        url="https://github.com/luaposix/luaposix/archive/refs/tags/v35.0.tar.gz",
    )
    version("36.1", sha256="5e48e8ea5adfd8958bcdbaba132f5766473afedecc5c14ae3593464a5463a616")
    version("33.4.0", sha256="e66262f5b7fe1c32c65f17a5ef5ffb31c4d1877019b4870a5d373e2ab6526a21")
    version("33.2.1", sha256="4fb34dfea67f4cf3194cdecc6614c9aea67edc3c4093d34137669ea869c358e1")

    depends_on("c", type="build")  # generated

    depends_on("lua-bit32", when="^lua-lang@5.1")
