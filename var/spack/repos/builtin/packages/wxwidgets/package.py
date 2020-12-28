# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Wxwidgets(AutotoolsPackage):
    """wxWidgets is a C++ library that lets developers create
       applications for Windows, Mac OS X, Linux and other platforms
       with a single code base. It has popular language bindings for
       Python, Perl, Ruby and many other languages, and unlike other
       cross-platform toolkits, wxWidgets gives applications a truly
       native look and feel because it uses the platform's native API
       rather than emulating the GUI. It's also extensive, free,
       open-source and mature."""

    homepage = "http://www.wxwidgets.org/"
    url      = "https://github.com/wxWidgets/wxWidgets/releases/download/v3.1.0/wxWidgets-3.1.0.tar.bz2"
    git      = "https://github.com/wxWidgets/wxWidgets.git"

    version('develop', branch='master')
    version('3.1.0', sha256='e082460fb6bf14b7dd6e8ac142598d1d3d0b08a7b5ba402fdbf8711da7e66da8')
    version('3.0.2', sha256='346879dc554f3ab8d6da2704f651ecb504a22e9d31c17ef5449b129ed711585d')
    version('3.0.1', sha256='bd671b79ec56af8fb3844e11cafceac1a4276fb02c79404d06b91b6c19d2c5f5')

    patch('math_include.patch', when='@3.0.1:3.0.2')

    depends_on('pkgconfig', type='build')
    depends_on('gtkplus')

    @when('@:3.0.2')
    def build(self, spec, prefix):
        make(parallel=False)

    def configure_args(self):
        spec = self.spec
        options = [
            '--enable-unicode',
            '--disable-precomp-headers'
        ]

        # see http://trac.wxwidgets.org/ticket/17639
        if spec.satisfies('@:3.1.0') and sys.platform == 'darwin':
            options.extend([
                '--disable-qtkit',
                '--disable-mediactrl'
            ])

        return options
