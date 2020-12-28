# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtommath(MakefilePackage):
    """A portable number theoretic multiple-precision integer library."""

    homepage = "http://www.libtom.net/"
    url      = "https://github.com/libtom/libtommath/archive/v1.2.0.tar.gz"

    version('1.2.0', sha256='f3c20ab5df600d8d89e054d096c116417197827d12732e678525667aa724e30f')
    version('1.1.0', sha256='71b6f3f99341b7693393ab4b58f03b79b6afc2ee5288666cc4538b4b336355f4')

    def install(self, spec, prefix):
        make('DESTDIR={0}'.format(prefix),
             'LIBPATH=/lib', 'INCPATH=/include', 'install')
