# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ConnectProxy(MakefilePackage):
    """`connect.c` is a simple relaying command to make network connection
    via SOCKS and https proxy"""

    homepage = "https://bitbucket.org/gotoh/connect"
    url      = "https://bitbucket.org/gotoh/connect/get/1.105.tar.bz2"

    version('1.105', sha256='07366026b1f81044ecd8da9b5b5b51321327ecdf6ba23576271a311bbd69d403')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('connect', prefix.bin)
