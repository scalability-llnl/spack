# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

import spack.build_systems.lua
from spack.package import *


class LuaLpeg(LuaPackage):
    """pattern-matching for lua"""

    homepage = "https://www.inf.puc-rio.br/~roberto/lpeg/"
    url = "https://luarocks.org/manifests/gvvaughan/lpeg-1.0.2-1.src.rock"

    license("MIT")

    version(
        "1.1.0-1",
        sha256="6637fcf4d3ddef7be490a2f0155bd2dcd053272d1bb78c015498709ef9fa75dd",
        expand=False,
    )
    version(
        "1.0.2-1",
        sha256="e0d0d687897f06588558168eeb1902ac41a11edd1b58f1aa61b99d0ea0abbfbc",
        expand=False,
    )
    version(
        "0.12-1",
        sha256="3962e8d695d0f9095c9453f2a42f9f1a89fb94db9b0c3bf22934c1e8a3b0ef5a",
        expand=False,
    )

    depends_on("lua-lang@:5.1.9", when="@:0.12.1 ^[virtuals=lua-lang] lua")


class LuaBuilder(spack.build_systems.lua.LuaBuilder):
    # without this, the resulting library cannot be linked by a normal link phase, the
    # way neovim expects to link it, works fine with lua loads though,
    # * replaces `-bundle` from the default flags with `-shared`
    @when("platform=darwin")
    def generate_luarocks_config(self, pkg, spec, prefix):
        path = super().generate_luarocks_config(pkg, spec, prefix)

        with open(path, "a") as cfg:
            cfg.write(
                """

            variables = {
                LIBFLAG = "-shared -fPIC -undefined dynamic_lookup -all_load"
            }
            """
            )

        return path

    # Builds searching for lpeg with darwin conventions can't find it without a dylib
    # symlink, neovim is an example
    @run_after("install", when="platform=darwin")
    def create_dylib_link_and_fix_id(self):
        lpeg_so = find(self.prefix, "lpeg.so")
        assert len(lpeg_so) >= 1
        dylib_path = os.path.join(self.prefix.lib, "liblpeg.dylib")
        symlink(lpeg_so[0], dylib_path)
        # can't use spack.filesystem.fix_darwin_install_name for this, doesn't work
        install_name_tool = which("install_name_tool", required=True)
        install_name_tool("-id", dylib_path, dylib_path)
