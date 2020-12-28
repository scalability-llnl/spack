# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class LuaLuafilesystem(Package):
    """LuaFileSystem is a Lua library developed to complement the set of
    functions related to file systems offered by the standard Lua distribution.

    LuaFileSystem offers a portable way to access the underlying directory
    structure and file attributes.

    LuaFileSystem is free software and uses the same license as Lua 5.1
    """

    homepage = 'http://keplerproject.github.io/luafilesystem'
    url = 'https://github.com/keplerproject/luafilesystem/archive/v1_6_3.tar.gz'

    version('1_7_0_2', sha256='23b4883aeb4fb90b2d0f338659f33a631f9df7a7e67c54115775a77d4ac3cc59')
    version('1_6_3', sha256='11c7b1fc2e560c0a521246b84e6257138d97dddde5a19e405714dbabcb9436ca')

    # The version constraint here comes from this post:
    #
    # https://www.perforce.com/blog/git-beyond-basics-using-shallow-clones
    #
    # where it is claimed that full shallow clone support was added @1.9
    depends_on('git@1.9.0:', type='build')
    extends('lua')

    @property
    def rockspec(self):
        version = self.spec.version
        semver = version[0:3]
        tweak_level = version[3] if len(version) > 3 else 1
        fmt = os.path.join(
            self.stage.source_path,
            'rockspecs',
            'luafilesystem-{semver.dotted}-{tweak_level}.rockspec'
        )
        return fmt.format(
            version=version, semver=semver, tweak_level=tweak_level
        )

    def install(self, spec, prefix):
        luarocks('--tree=' + prefix, 'make', self.rockspec)
