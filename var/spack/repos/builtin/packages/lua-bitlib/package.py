# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class LuaBitlib(LuaPackage):
    """Lua-jit-like bitwise operations for lua"""

    homepage = "https://luaforge.net/projects/bitlib"
    url = "https://luarocks.org/manifests/luarocks/bitlib-23-2.src.rock"

    version(
        "23-2",
        sha256="fe226edc2808162e67418e6b2c98befc0ed25a489ecffc6974fa153f951c0c34",
        expand=False,
    )

    def preprocess(self, spec, prefix):
        m = FileFilter("lbitlib.c")
        m.filter("luaL_reg", "luaL_Reg")
