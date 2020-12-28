# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libluv(CMakePackage):
    """This library makes libuv available to lua scripts.
    It was made for the luvit project but should usable from nearly
    any lua project."""

    homepage = "https://github.com/luvit/luv"
    url      = "https://github.com/luvit/luv/releases/download/1.36.0-0/luv-1.36.0-0.tar.gz"

    version('1.36.0-0', sha256='f2e7eb372574f25c6978c1dc74280d22efdcd7df2dda4a286c7fe7dceda26445')

    depends_on('lua', type='link')
    depends_on('libuv', type='link')

    def cmake_args(self):
        args = [
            '-DLUA_BUILD_TYPE=System',
            '-DBUILD_STATIC_LIBS=ON',
            '-DBUILD_SHARED_LIBS=ON',
            '-DWITH_SHARED_LIBUV=ON',
            '-DWITH_LUA_ENGINE=Lua',
        ]
        return args
