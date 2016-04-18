##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

class Cmake(Package):
    """A cross-platform, open-source build system. CMake is a family of
       tools designed to build, test and package software."""
    homepage  = 'https://www.cmake.org'
    url       = 'https://cmake.org/files/v3.4/cmake-3.4.3.tar.gz'

    version('3.5.2',    '701386a1b5ec95f8d1075ecf96383e02')
    version('3.5.1',    'ca051f4a66375c89d1a524e726da0296')
    version('3.5.0',    '33c5d09d4c33d4ffcc63578a6ba8777e')
    version('3.4.3',    '4cb3ff35b2472aae70f542116d616e63')
    version('3.4.0',    'cd3034e0a44256a0917e254167217fc8')
    version('3.3.1',    '52638576f4e1e621fed6c3410d3a1b12')
    version('3.0.2',    'db4c687a31444a929d2fdc36c4dfb95f')
    version('2.8.10.2', '097278785da7182ec0aea8769d06860c')

    variant('ncurses', default=True, description='Enables the build of the ncurses gui')
    variant('openssl', default=True, description="Enables CMake's OpenSSL features")
    variant('doc', default=False, description='Enables the generation of html and man page documentation')

    depends_on('ncurses', when='+ncurses')
    depends_on('openssl', when='+openssl')
    depends_on('python@2.7.11:', when='+doc')
    depends_on('py-sphinx', when='+doc')

    def url_for_version(self, version):
        """Handle CMake's version-based custom URLs."""
        return 'https://cmake.org/files/v%s/cmake-%s.tar.gz' % (version.up_to(2), version)

    def install(self, spec, prefix):

        # configure, build, install:
        options = ['--prefix=%s' % prefix]
        options.append('--parallel=%s' % str(make_jobs))

        if '+doc' in spec:
            options.append('--sphinx-html')
            options.append('--sphinx-man')

        if '+openssl' in spec:
            options.append('--')
            options.append('-DCMAKE_USE_OPENSSL=ON')

        configure(*options)
        make()
        make('install')
