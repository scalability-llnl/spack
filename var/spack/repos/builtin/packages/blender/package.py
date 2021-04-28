# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Blender(CMakePackage):
    """Blender is the free and open source 3D creation suite.
    It supports the entirety of the 3D pipeline-modeling,
    rigging, animation, simulation, rendering, compositing and
    motion tracking, even video editing and game creation."""

    homepage = "https://www.blender.org/"
    url      = "http://download.blender.org/source/blender-2.79b.tar.gz"

    version('2.92.0',
            url='https://download.blender.org/source/blender-2.92.0.tar.xz',
            sha256='e791cfc403292383577c3c8ce2cd34e5aa2cd8da0a7483041049a1609ddb4595')
    version('2.80', sha256='cd9d7e505c1f6e63a4f72366ed04d446859977eeb34cde21283aaea6a304a5c0')
    version('2.79b', sha256='4c944c304a49e68ac687ea06f5758204def049b66dc211e1cffa1857716393bc')

    variant('cycles', default=False, description='Build with cycles support')
    variant('blender', default=True, description='disable to build only the blender player')
    variant('player', default=True, description='Build Player')
    variant('ffmpeg', default=False, description='Enable FFMPeg Support')
    variant('headless', default=False, description='Build without graphical support (renderfarm, server mode only)')
    variant('llvm', default=False, description='Necessary for OSL.')
    variant('ocio', default=False, description='Currently broken due to conflicting python')
    variant('opensubdiv', default=False, description='Build with opensubdiv support')
    variant('jemalloc', default=True)

    # https://developer.blender.org/diffusion/B/browse/blender-v2.92-release/build_files/build_environment/cmake/versions.cmake
    depends_on('python@3.5:', when="@:2.79b")
    depends_on('python@3.7:', when="@2.80:")
    depends_on('python@3.7.7:', when="@2.92.0:")

    depends_on('py-numpy', when="@2.80:")
    depends_on('py-numpy@1.17.5:', when='@2.92.0:')
    
    depends_on('glew')
    depends_on('glew@1.13.0:', when='@2.92.0:')

    #depends_on('opengl')
    # depends_on('openglu')
    depends_on('gl')
    depends_on('glu')
    depends_on('glx')
    
    depends_on('libpng')
    depends_on('libpng@1.6.37:', when='@2.92.0:')

    depends_on('libjpeg')
    depends_on('libjpeg@2.0.4:', when='@2.92.0:')

    depends_on('openjpeg')
    depends_on('openjpeg@2.3.1:', when='@2.92.0:')

#     depends_on('boost@1.49:1.69')
    depends_on('boost@1.70.0:', when='@2.92.0:')

    depends_on('openimageio', when='+cycles')
    depends_on('openimageio@2.1.15.0:', when='@2.92.0: +cycles')

    # Upper bound per: https://developer.blender.org/T54779
    depends_on('ffmpeg@3.2.1:3.999', when='@:2.79b+ffmpeg')
    depends_on('ffmpeg@3.2.1:', when='@2.80:+ffmpeg')
    depends_on('ffmpeg@4.2.3:', when='@2.92.0:+ffmpeg')

#    depends_on('opencolorio@1.0:', when='+ocio')

    depends_on('llvm@3.0:', when='+llvm')
    depends_on('llvm@9.0.1:', when='@2.92.0:+llvm')
    # depends_on('openshadinglanguage')
    # depends_on('openvdb@3.1:')

    # FIXME: this is only temporarily commented out. needs to be fixed
    # depends_on('freetype')
    depends_on('freetype@2.10.2:', when='@2.92.0:')

    depends_on('libuuid')
    depends_on('jemalloc', when='+jemalloc')
    depends_on('ilmbase')

    depends_on('opensubdiv+openmp', when='+opensubdiv')
    depends_on('opensubdiv@3.4.3:', when='@2.92.0:+opensubdiv')
    
    #depends_on('cuda@10.1.0:10.1.999', when='+cycles', type=('link','run'))
    depends_on('cuda@11.0:', when='@2.92.0:+cycles', type=('link','run'))
    # FIXME: The version of GCC should probably be the version of GCC that is actually
    # compiling blender, not hardcoding the version that the package creater is using. 
#     depends_on('gcc@7.4.0', when='+cycles', type=('run'))


    # Dependencies for 2.92.0
    depends_on('zlib@1.2.11:', when='@2.92.0:')
    depends_on('openal-soft@1.20.1:', when='@2.92.0:')
    depends_on('c-blosc@1.5.0:', when='@2.92.0:')
#     depends_on('pthreads@3.0.0:', when='@2.92.0:')
#     depends_on('openexr@2.4.0:', when='@2.92.0:')
#     depends_on('freeglut@3.0.0:', when='@2.92.0:')
    depends_on('alembic@1.7.12:', when='@2.92.0:')
#     depends_on('glfw@3.1.2:', when='@2.92.0:')
#     depends_on('sdl@2.0.12:', when='@2.92.0:')
#     depends_on('opencollada@1.6.68:', when='@2.92.0:')
#     depends_on('opencolorio@1.1.1:', when='@2.92.0:')
    depends_on('libtiff@4.1.0:', when='@2.92.0:')
#     depends_on('openshadinglanguage@1.10.10:', when='@2.92.0:')
#     depends_on('tbb@2019_u9:', when='@2.92.0:')
#     depends_on('openvdb@7.0.0:', when='@2.92.0:')
#     depends_on('idna@2.9:', when='@2.92.0:')
#     depends_on('lame@3.100:', when='@2.92.0:')
    depends_on('libogg@1.3.4:', when='@2.92.0:')
    depends_on('libvorbis@1.3.6:', when='@2.92.0:')
    depends_on('libtheora@1.1.1:', when='@2.92.0:')
    depends_on('flac@1.3.3:', when='@2.92.0:')
#     depends_on('vpx@1.8.2:', when='@2.92.0:')
    depends_on('opus@1.3.1:', when='@2.92.0:')
#     depends_on('xvidcore@1.3.7:', when='@2.92.0:')
    depends_on('fftw@3.3.8:', when='@2.92.0:')
    depends_on('libiconv@1.16:', when='@2.92.0:')
    depends_on('libsndfile@1.0.28:', when='@2.92.0:')
    # sndfile

    # FIXME: ~ispc is temporary fix for
    # ispc requires llvm variant ~libcxx, but spec asked for +libcxx
    depends_on('embree@3.10.0:~ispc', when='@2.92.0:')

    depends_on('pugixml@1.10:', when='@2.92.0:')

    depends_on('gmp@6.2.0:', when='@2.92.0:')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', os.path.dirname(self.compiler.cc))

    def cmake_args(self):
        spec = self.spec
        args = []

        python_exe = spec['python'].command.path
        python_lib = spec['python'].libs[0]
        python_include_dir = spec['python'].headers.directories[0]

        args.append('-DPYTHON_EXECUTABLE={0}'.format(python_exe))
        args.append('-DPYTHON_LIBRARY={0}'.format(python_lib))
        args.append('-DPYTHON_INCLUDE_DIR={0}'.format(python_include_dir))
        args.append('-DPYTHON_VERSION={0}'.format(spec['python'].version.up_to(2)))

        args.append('-DWITH_INSTALL_PORTABLE=NO')

        args.append('-DCMAKE_CXX_FLAGS=-I{0}/include/OpenEXR'.format(spec['ilmbase'].prefix))

        if '@2.8:' in spec:
            args.append(
                '-DPYTHON_NUMPY_PATH:PATH={0}/python{1}/site-packages'.format(
                    spec['py-numpy'].prefix.lib,
                    spec['python'].version.up_to(2)))
            args.append(
                '-DPYTHON_NUMPY_INCLUDE_DIRS:PATH={0}/python{1}/site-packages/numpy/core/include'.format(
                    spec['py-numpy'].prefix.lib,
                    spec['python'].version.up_to(2)))

        if '+opensubdiv' in spec:
            args.append('-DWITH_OPENSUBDIV:BOOL=ON')
        else:
            args.append('-DWITH_OPENSUBDIV:BOOL=OFF')

        if '~cycles' in spec:
            args.append('-DWITH_CYCLES:BOOL=OFF')

        if '~blender' in spec:
            args.append('-DWITH_BLENDER:BOOL=OFF')
            # UNTESTED

        if '+ffmpeg' in spec:
            args.append('-DWITH_CODEC_FFMPEG:BOOL=ON')

        if '+headless' in spec:
            args.append('-DWITH_HEADLESS:BOOL=OFF')

        if '+llvm' in spec:
            args.append('-DWITH_LLVM:BOOL=ON')

        if '+player' in spec:
            args.append('-DWITH_PLAYER:BOOL=ON')

# >> 106    CMake Error at CMakeLists.txt:924 (message):
#    107      WITH_MOD_OCEANSIM requires WITH_FFTW3 to be ON
        if self.spec.satisfies('@2.92.0:'):
            args.append('-DWITH_MOD_OCEANSIM:BOOL=OFF')

        return args
