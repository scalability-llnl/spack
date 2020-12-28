# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openscenegraph(CMakePackage):
    """OpenSceneGraph is an open source, high performance 3D graphics toolkit
       that's used in a variety of visual simulation applications."""

    homepage = "http://www.openscenegraph.org"
    git      = "https://github.com/openscenegraph/OpenSceneGraph.git"
    url      = "https://github.com/openscenegraph/OpenSceneGraph/archive/OpenSceneGraph-3.6.4.tar.gz"

    version('3.6.5', sha256='aea196550f02974d6d09291c5d83b51ca6a03b3767e234a8c0e21322927d1e12')
    version('3.6.4', sha256='81394d1b484c631028b85d21c5535280c21bbd911cb058e8746c87e93e7b9d33')
    version('3.4.1', sha256='930eb46f05781a76883ec16c5f49cfb29a059421db131005d75bec4d78401fd5')
    version('3.4.0', sha256='0d5efe12b923130d14a6fce5866675d7625fcfb1c004c9f9b10034b9feb61ac2')
    version('3.2.3', sha256='a1ecc6524197024834e1277916922b32f30246cb583e27ed19bf3bf889534362')
    version('3.1.5', sha256='dddecf2b33302076712100af59b880e7647bc595a9a7cc99186e98d6e0eaeb5c')

    variant('shared', default=True, description='Builds a shared version of the library')
    variant('ffmpeg', default=False, description='Builds ffmpeg plugin for audio encoding/decoding')

    depends_on('cmake@2.8.7:', type='build')
    depends_on('gl')
    depends_on('qt+opengl', when='@:3.5.4')  # Qt windowing system was moved into separate osgQt project
    depends_on('qt@4:', when='@3.2:3.5.4')
    depends_on('qt@:4', when='@:3.1')
    depends_on('libxinerama')
    depends_on('libxrandr')
    depends_on('libpng')
    depends_on('jasper')
    depends_on('libtiff')
    depends_on('glib')
    depends_on('zlib')

    depends_on('ffmpeg+avresample', when='+ffmpeg')
    # https://github.com/openscenegraph/OpenSceneGraph/issues/167
    depends_on('ffmpeg@:2', when='@:3.4.0+ffmpeg')

    patch('glibc-jasper.patch', when='@3.4%gcc')

    def cmake_args(self):
        spec = self.spec

        shared_status = 'ON' if '+shared' in spec else 'OFF'
        opengl_profile = 'GL{0}'.format(spec['gl'].version.up_to(1))

        args = [
            # Variant Options #
            '-DDYNAMIC_OPENSCENEGRAPH={0}'.format(shared_status),
            '-DDYNAMIC_OPENTHREADS={0}'.format(shared_status),
            '-DOPENGL_PROFILE={0}'.format(opengl_profile),

            # General Options #
            '-DBUILD_OSG_APPLICATIONS=OFF',
            '-DOSG_NOTIFY_DISABLED=ON',
            '-DLIB_POSTFIX=',
            '-DCMAKE_RELWITHDEBINFO_POSTFIX=',
            '-DCMAKE_MINSIZEREL_POSTFIX='
        ]

        if spec.satisfies('~ffmpeg'):
            for ffmpeg_lib in ['libavcodec', 'libavformat', 'libavutil']:
                args.extend([
                    '-DFFMPEG_{0}_INCLUDE_DIRS='.format(ffmpeg_lib.upper()),
                    '-DFFMPEG_{0}_LIBRARIES='.format(ffmpeg_lib.upper()),
                ])

        # NOTE: This is necessary in order to allow OpenSceneGraph to compile
        # despite containing a number of implicit bool to int conversions.
        if spec.satisfies('%gcc'):
            args.extend([
                '-DCMAKE_C_FLAGS=-fpermissive',
                '-DCMAKE_CXX_FLAGS=-fpermissive',
            ])

        return args
