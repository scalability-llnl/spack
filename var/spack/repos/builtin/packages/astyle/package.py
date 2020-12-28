# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Astyle(MakefilePackage):
    """A Free, Fast, and Small Automatic Formatter for C, C++, C++/CLI,
    Objective-C, C#, and Java Source Code.
    """

    homepage = "http://astyle.sourceforge.net/"
    url = "https://sourceforge.net/projects/astyle/files/astyle/astyle%203.0.1/astyle_3.0.1_linux.tar.gz"
    # Gentoo alternative
    # url = "http://distfiles.gentoo.org/distfiles/astyle_3.0.1_linux.tar.gz"

    version('3.1',    sha256='cbcc4cf996294534bb56f025d6f199ebfde81aa4c271ccbd5ee1c1a3192745d7')
    version('3.0.1',  sha256='6c3ab029e0e4a75e2e603d449014374aa8269218fdd03a4aaa46ab743b1912fd')
    version('2.06',   sha256='3b7212210dc139e8f648e004b758c0be1b3ceb1694b22a879202d2b833db7c7e')
    version('2.05.1', sha256='fbdfc6f1966a972d19a215927266c76d4183eee235ed1e2bd7ec551c2a270eac')
    version('2.04',   sha256='70b37f4853c418d1e2632612967eebf1bdb93dfbe558c51d7d013c9b4e116b60')

    parallel = False

    @property
    def build_directory(self):
        return join_path(self.stage.source_path, 'build', self.compiler.name)

    def edit(self, spec, prefix):
        makefile = join_path(self.build_directory, 'Makefile')
        filter_file(r'^CXX\s*=.*', 'CXX=%s' % spack_cxx, makefile)
        # strangely enough install -o $(USER) -g $(USER) stoped working on OSX
        if sys.platform == 'darwin':
            filter_file(r'^INSTALL=.*', 'INSTALL=install', makefile)

    @property
    def install_targets(self):
        return ['install', 'prefix={0}'.format(self.prefix)]
