# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.build_systems.lua
from spack.package import *


class LuaLuafilesystem(LuaPackage):
    """LuaFileSystem is a Lua library developed to complement the set of
    functions related to file systems offered by the standard Lua distribution.

    LuaFileSystem offers a portable way to access the underlying directory
    structure and file attributes.

    LuaFileSystem is free software and uses the same license as Lua 5.1
    """

    homepage = "https://lunarmodules.github.io/luafilesystem/"

    def url_for_version(self, version):
        url = "https://github.com/lunarmodules/luafilesystem/archive/refs/tags/v{0}.tar.gz"
        return url.format(version.underscored)

    license("MIT")

    version("1.8.0", sha256="16d17c788b8093f2047325343f5e9b74cccb1ea96001e45914a58bbae8932495")
    version("1.7.0-2", sha256="23b4883aeb4fb90b2d0f338659f33a631f9df7a7e67c54115775a77d4ac3cc59")
    version("1.6.3", sha256="11c7b1fc2e560c0a521246b84e6257138d97dddde5a19e405714dbabcb9436ca")

    depends_on("c", type="build")  # generated

    depends_on("lua-lang@:5.3", when="@:1.7")


class LuaBuilder(spack.build_systems.lua.LuaBuilder):
    def install(self, pkg, spec, prefix):
        rocks_args = self.luarocks_args()
        if spec.satisfies("@:1.7.0-2"):
            rock = "rockspecs/luafilesystem-{0}.rockspec".format(self.spec.version)
            if not os.path.isfile(rock):
                rock = "rockspecs/luafilesystem-{0}-1.rockspec".format(self.spec.version)
            if not os.path.isfile(rock):
                # fall back on default luarocks behavior for finding rockspec
                rock = ""
            rocks_args.append(rock)
        self.pkg.luarocks("--tree=" + prefix, "make", *rocks_args)
