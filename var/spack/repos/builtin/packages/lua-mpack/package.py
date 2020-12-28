# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class LuaMpack(Package):
    """lua bindings to libmpack"""

    homepage = "https://luarocks.org/modules/tarruda/mpack"
    url      = "https://luarocks.org/manifests/tarruda/mpack-1.0.6-0.src.rock"

    depends_on('msgpack-c')

    version('1.0.6-0', sha256='9068d9d3f407c72a7ea18bc270b0fa90aad60a2f3099fa23d5902dd71ea4cd5f',
            expand=False)

    extends('lua')

    def install(self, spec, prefix):
        luarocks('--tree=' + prefix, 'install', 'mpack-1.0.6-0.src.rock')
