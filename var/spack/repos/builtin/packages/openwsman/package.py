# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Openwsman(CMakePackage):
    """Openwsman server implementation and client api with bindings."""

    homepage = "https://github.com/Openwsman/openwsman"
    url      = "https://github.com/Openwsman/openwsman/archive/v2.6.11.tar.gz"

    version('2.7.0',  sha256='8870c4a21cbaba9387ad38c37667e2cee29008faacaaf7eb18ad2061e2fc89a1')
    version('2.6.11', sha256='895eaaae62925f9416766ea3e71a5368210e6cfe13b23e4e0422fa0e75c2541c')
    version('2.6.10', sha256='d3c624a03d7bc1835544ce1af56efd010f77cbee0c02b34e0755aa9c9b2c317b')

    variant('python', default=True, description='Enable python')

    extends('python', when='+python')

    depends_on('python', type=('build', 'link', 'run'))
    depends_on('curl', type='link')
    depends_on('swig', type='build')
    depends_on('libxml2', type='link')
    depends_on('openssl', type='link')
    depends_on('sblim-sfcc', type='link')

    def patch(self):
        """ Change python install directory. """
        if self.spec.satisfies('+python'):
            python_spec = self.spec['python']
            python_libdir = join_path(
                self.spec.prefix.lib,
                'python' + str(python_spec.version.up_to(2)),
                'site-packages'
            )
            filter_file(
                'DESTINATION .*',
                'DESTINATION {0} )'.format(python_libdir),
                join_path('bindings', 'python', 'CMakeLists.txt')
            )

    def cmake_args(self):
        define = self.define
        spec = self.spec
        arg = [
            define('BUILD_PERL', False),
            define('BUILD_JAVA', False),
            define('BUILD_CSHARP', False),
            define('USE_PAM', 'OFF'),
        ]
        if spec.satisfies('+python'):
            if spec.satisfies('^python@3:'):
                arg.extend([
                    define('BUILD_PYTHON', False),
                    define('BUILD_PYTHON3', True)
                ])
            else:
                arg.extend([
                    define('BUILD_PYTHON', True),
                    define('BUILD_PYTHON3', False)
                ])
            arg.append(define('PYTHON_EXECUTABLE',
                       spec['python'].command.path))
        else:
            arg.extend([
                define('BUILD_PYTHON', False),
                define('BUILD_PYTHON3', False)
            ])
        return arg

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cflags':
            if self.spec.satisfies('%gcc'):
                flags.append('-std=gnu99')
            else:
                flags.append(self.compiler.c99_flag)
        return (None, None, flags)
