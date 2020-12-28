# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class LuaBitlib(Package):
    """Lua-jit-like bitwise operations for lua"""

    homepage = "http://luaforge.net/projects/bitlib"
    url      = "https://luarocks.org/bitlib-23-2.src.rock"

    version('23-2', sha256='fe226edc2808162e67418e6b2c98befc0ed25a489ecffc6974fa153f951c0c34',
            expand=False)

    extends('lua')

    def install(self, spec, prefix):
        luarocks('unpack', "bitlib-23-2.src.rock")
        os.chdir(os.path.join('bitlib-23-2', 'bitlib-23'))
        sed = which('sed')
        sed('-ie', 's/luaL_reg/luaL_Reg/', 'lbitlib.c')
        luarocks('--tree=' + prefix, 'make')
