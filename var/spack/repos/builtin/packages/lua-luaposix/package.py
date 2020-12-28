# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class LuaLuaposix(Package):
    """Lua posix bindings, including ncurses"""
    homepage = "https://github.com/luaposix/luaposix/"
    url      = "https://github.com/luaposix/luaposix/archive/release-v33.4.0.tar.gz"

    version('33.4.0', sha256='e66262f5b7fe1c32c65f17a5ef5ffb31c4d1877019b4870a5d373e2ab6526a21')
    version('33.2.1', sha256='4fb34dfea67f4cf3194cdecc6614c9aea67edc3c4093d34137669ea869c358e1')

    extends("lua")

    def install(self, spec, prefix):
        rockspec = glob.glob('luaposix-*.rockspec')
        luarocks('--tree=' + prefix, 'make', rockspec[0])
