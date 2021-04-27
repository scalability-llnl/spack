# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fltk(Package):
    """FLTK (pronounced "fulltick") is a cross-platform C++ GUI toolkit for
       UNIX/Linux (X11), Microsoft Windows, and MacOS X. FLTK provides
       modern GUI functionality without the bloat and supports 3D
       graphics via OpenGL and its built-in GLUT emulation.

       FLTK is designed to be small and modular enough to be statically
       linked, but works fine as a shared library. FLTK also includes an
       excellent UI builder called FLUID that can be used to create
       applications in minutes.

    """
    homepage = 'http://www.fltk.org/'
    url = 'http://fltk.org/pub/fltk/1.3.3/fltk-1.3.3-source.tar.gz'

    version('1.3.3', sha256='f8398d98d7221d40e77bc7b19e761adaf2f1ef8bb0c30eceb7beb4f2273d0d97')

    depends_on('libx11')

    patch('font.patch', when='@1.3.3')

    # https://github.com/fltk/fltk/commits/master/src/Fl_Tree_Item.cxx
    #  -Fix return value test, as pointed out by Albrecht.
    patch('fix_compare_val.patch', when='@:1.3.3')
    # https://github.com/fltk/fltk/commits/master/test/menubar.cxx
    # -Allow compilation with -std=c++11
    # -Add missing cast (part of patch for STR #2813).
    patch('type_cast.patch', when='@:1.3.3')

    variant('shared', default=True,
            description='Enables the build of shared libraries')

    variant('gl', default=True,
            description='Enables opengl support')

    # variant dependencies
    depends_on('gl', when='+gl')

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix,
                   '--enable-localjpeg',
                   '--enable-localpng',
                   '--enable-localzlib']

        if '+shared' in spec:
            options.append('--enable-shared')

        if '~gl' in spec:
            options.append('--disable-gl')

        # FLTK needs to be built in-source
        configure(*options)
        make()
        make('install')

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies('%nvhpc'):
            filter_file('OPTIM="-Wall -Wunused -Wno-format-y2k $OPTIM"',
                        'OPTIM="-Wall $OPTIM"', 'configure', string=True)
            filter_file('OPTIM="-Os $OPTIM"', 'OPTIM="-O2 $OPTIM"',
                        'configure', string=True)
            filter_file('CXXFLAGS="$CXXFLAGS -fvisibility=hidden"',
                        'CXXFLAGS="$CXXFLAGS"', 'configure', string=True)
            filter_file('OPTIM="$OPTIM -fvisibility=hidden"',
                        'OPTIM="$OPTIM"', 'configure', string=True)
