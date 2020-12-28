# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Symlinks(MakefilePackage):
    """Scan or change symbolic links."""

    homepage = "http://ibiblio.org/pub/Linux/utils/file"
    url      = "http://ibiblio.org/pub/Linux/utils/file/symlinks-1.4.tar.gz"

    version('1.4', sha256='4818a3be253b53f2547fe51349652c87301794fc2ff4e3104850301ffe9843a0')

    def edit(self, spec, prefix):
        filter_file('/usr/local', prefix, 'Makefile', string=True)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man8)
        make('install')
