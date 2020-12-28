# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jasper(Package):
    """Library for manipulating JPEG-2000 images"""

    homepage = "https://www.ece.uvic.ca/~frodo/jasper/"
    url      = "https://github.com/mdadams/jasper/archive/version-2.0.16.tar.gz"

    version('2.0.16',  sha256='f1d8b90f231184d99968f361884e2054a1714fdbbd9944ba1ae4ebdcc9bbfdb1')
    version('2.0.14',  sha256='85266eea728f8b14365db9eaf1edc7be4c348704e562bb05095b9a077cf1a97b')
    version('1.900.1', sha256='c2b03f28166f9dc8ae434918839ae9aa9962b880fcfd24eebddd0a2daeb9192c')

    variant('jpeg',   default=True,  description='Enable the use of the JPEG library')
    variant('opengl', default=False, description='Enable the use of the OpenGL and GLUT libraries')
    variant('shared', default=True,  description='Enable the building of shared libraries')
    variant('build_type', default='Release', description='CMake build type', values=('Debug', 'Release'))

    depends_on('cmake@2.8.11:', type='build', when='@2:')
    depends_on('jpeg', when='+jpeg')
    depends_on('gl', when='+opengl')

    # Fixes a bug where an assertion fails when certain JPEG-2000
    # files with an alpha channel are processed.
    # See: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=469786
    patch('fix_alpha_channel_assert_fail.patch', when='@1.900.1')

    def cmake_args(self):
        spec = self.spec
        args = std_cmake_args
        args.append('-DJAS_ENABLE_DOC=false')

        if '+jpeg' in spec:
            args.append('-DJAS_ENABLE_LIBJPEG=true')
        else:
            args.append('-DJAS_ENABLE_LIBJPEG=false')

        if '+opengl' in spec:
            args.append('-DJAS_ENABLE_OPENGL=true')
        else:
            args.append('-DJAS_ENABLE_OPENGL=false')

        if '+shared' in spec:
            args.append('-DJAS_ENABLE_SHARED=true')
        else:
            args.append('-DJAS_ENABLE_SHARED=false')

        return args

    def configure_args(self):
        spec = self.spec
        args = [
            '--prefix={0}'.format(self.prefix)
        ]

        if '+jpeg' in spec:
            args.append('--enable-libjpeg')
        else:
            args.append('--disable-libjpeg')

        if '+opengl' in spec:
            args.append('--enable-opengl')
        else:
            args.append('--disable-opengl')

        if '+shared' in spec:
            args.append('--enable-shared')
        else:
            args.append('--disable-shared')

        if 'build_type=Debug' in spec:
            args.append('--enable-debug')
        else:
            args.append('--disable-debug')

        return args

    @when('@2:')
    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *self.cmake_args())
            make()
            if self.run_tests:
                make('test')
            make('install')

    @when('@:1')
    def install(self, spec, prefix):
        configure(*self.configure_args())
        make()
        if self.run_tests:
            make('check')
        make('install')
        if self.run_tests:
            make('installcheck')
