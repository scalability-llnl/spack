# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Antlr(AutotoolsPackage):
    """ANTLR (ANother Tool for Language Recognition) is a powerful parser
    generator for reading, processing, executing, or translating structured
    text or binary files. It's widely used to build languages, tools, and
    frameworks. From a grammar, ANTLR generates a parser that can build and
    walk parse trees."""

    homepage = "http://www.antlr2.org/"
    url      = "http://www.antlr2.org/download/antlr-2.7.7.tar.gz"

    version('2.7.7', sha256='853aeb021aef7586bda29e74a6b03006bcb565a755c86b66032d8ec31b67dbb9')

    # Fixes build with recent versions of GCC
    patch('gcc.patch')

    variant('cxx',    default=True,  description='Enable ANTLR for C++')
    variant('java',   default=False, description='Enable ANTLR for Java')
    variant('python', default=False, description='Enable ANTLR for Python')

    extends('python', when='+python')
    depends_on('java', type=('build', 'run'), when='+java')

    def configure_args(self):
        spec = self.spec

        return [
            '--disable-csharp',
            '--{0}-cxx'.format('enable' if '+cxx' in spec else 'disable'),
            '--{0}-java'.format('enable' if '+java' in spec else 'disable'),
            '--{0}-python'.format('enable' if '+python' in spec else 'disable')
        ]
