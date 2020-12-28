# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack.package import *


class Re2c(AutotoolsPackage):
    """re2c: a free and open-source lexer generator for C and C++"""

    homepage = "http://re2c.org/index.html"
    url      = "https://github.com/skvadrik/re2c/releases/download/1.2.1/re2c-1.2.1.tar.xz"

    version('1.2.1', sha256='1a4cd706b5b966aeffd78e3cf8b24239470ded30551e813610f9cd1a4e01b817')

    def configure_args(self):
        args = ['--disable-dependency-tracking']
        return args
