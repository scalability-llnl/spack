# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.operating_systems.mac_os import macos_version
from spack.package import *


class Oce(Package):
    """Open CASCADE Community Edition:
    patches/improvements/experiments contributed by users over the official
    Open CASCADE library.
    """
    homepage = "https://github.com/tpaviot/oce"
    url = "https://github.com/tpaviot/oce/archive/OCE-0.18.tar.gz"

    version('0.18.3', sha256='c553d6a7bf52f790abc3b6bb7a1e91a65947e92a426bb1a88a11960c31f0966c')
    version('0.18.2', sha256='dc21ddea678a500ad87c773e9a502ed7a71768cf83d9af0bd4c43294186a7fef')
    version('0.18.1', sha256='1acf5da4bffa3592ca9f3535af9b927b79fcfeadcb81e9963e89aec192929a6c')
    version('0.18',   sha256='226e45e77c16a4a6e127c71fefcd171410703960ae75c7ecc7eb68895446a993')
    version('0.17.2', sha256='8d9995360cd531cbd4a7aa4ca5ed969f08ec7c7a37755e2f3d4ef832c1b2f56e')
    version('0.17.1', sha256='b1ff0cb8cf31339bbb30ac7ed2415d376b9b75810279d2f497e115f08c090928')
    version('0.17',   sha256='9ab0dc2a2d125b46cef458b56c6d171dfe2218d825860d616c5ab17994b8f74d')
    version('0.16.1', sha256='d31030c8da4a1b33f767d0d59895a995c8eabc8fc65cbe0558734f6021ea2f57')
    version('0.16',   sha256='841fe4337a5a4e733e36a2efc4fe60a4e6e8974917028df05d47a02f59787515')

    variant('tbb', default=True,
            description='Build with Intel Threading Building Blocks')
    variant('X11', default=False,
            description='Build with X11 enabled')

    depends_on('cmake@2.8:', type='build')
    depends_on('tbb', when='+tbb')

    # There is a bug in OCE which appears with Clang (version?) or GCC 6.0
    # and has to do with compiler optimization, see
    # https://github.com/tpaviot/oce/issues/576
    # http://tracker.dev.opencascade.org/view.php?id=26042
    # https://github.com/tpaviot/oce/issues/605
    # https://github.com/tpaviot/oce/commit/61cb965b9ffeca419005bc15e635e67589c421dd.patch
    patch('null.patch', when='@0.16:0.17.1')

    # OCE depends on xlocale.h from glibc-headers but it was removed in 2.26,
    # see https://github.com/tpaviot/oce/issues/675
    patch('xlocale.patch', level=0, when='@0.18.1:0.18.2')

    # fix build with Xcode 8 "previous definition of CLOCK_REALTIME"
    # reported 27 Sep 2016 https://github.com/tpaviot/oce/issues/643
    if (platform.system() == "Darwin") and (
       macos_version() == Version('10.12')):
        patch('sierra.patch', when='@0.17.2:0.18.0')

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)
        options.extend([
            '-DOCE_INSTALL_PREFIX=%s' % prefix,
            '-DOCE_BUILD_SHARED_LIB:BOOL=ON',
            '-DCMAKE_BUILD_TYPE:STRING=Release',
            '-DOCE_DATAEXCHANGE:BOOL=ON',
            '-DOCE_DISABLE_X11:BOOL=%s' % (
                'OFF' if '+X11' in spec else 'ON'),
            '-DOCE_DRAW:BOOL=OFF',
            '-DOCE_MODEL:BOOL=ON',
            '-DOCE_MULTITHREAD_LIBRARY:STRING=%s' % (
                'TBB' if '+tbb' in spec else 'NONE'),
            '-DOCE_OCAF:BOOL=ON',
            '-DOCE_USE_TCL_TEST_FRAMEWORK:BOOL=OFF',
            '-DOCE_VISUALISATION:BOOL=OFF',
            '-DOCE_WITH_FREEIMAGE:BOOL=OFF',
            '-DOCE_WITH_GL2PS:BOOL=OFF',
            '-DOCE_WITH_OPENCL:BOOL=OFF'
        ])

        if platform.system() == 'Darwin':
            options.extend([
                '-DOCE_OSX_USE_COCOA:BOOL=ON',
            ])

        if platform.system() == 'Darwin' and (
           macos_version() >= Version('10.12')):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append('-DCMAKE_MACOSX_RPATH=ON')
        else:
            options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)

        cmake('.', *options)
        make("install/strip")
        if self.run_tests:
            make("test")
