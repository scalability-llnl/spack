# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys


class Mesa18(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL specification
     - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    maintainers = ['v-dobrev', 'chuckatkins']

    # Note that we always want to build from the git repo instead of a
    # tarball since the tarball has pre-generated files for certain versions
    # of LLVM while the git repo doesn't so it can adapt at build time to
    # whatever version of LLVM you're using.
    git      = "https://gitlab.freedesktop.org/mesa/mesa.git"

    version('18.3.6', tag='mesa-18.3.6', preferred=True)

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('binutils', when=(sys.platform != 'darwin'), type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('gettext', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python', type='build')
    depends_on('py-mako@0.8.0:', type='build')
    depends_on('libxml2')
    depends_on('zlib')
    depends_on('expat')
    depends_on('ncurses+termlib')

    # Internal options
    variant('llvm', default=True, description="Enable LLVM.")
    variant('swr', values=any_combination_of('avx', 'avx2', 'knl', 'skx'),
            description="Enable the SWR driver.")
    # conflicts('~llvm', when='~swr=none')

    # Front ends
    variant('osmesa', default=True, description="Enable the OSMesa frontend.")

    is_linux = sys.platform.startswith('linux')
    variant('glx', default=is_linux, description="Enable the GLX frontend.")

    # TODO: effectively deal with EGL.  The implications of this have not been
    # worked through yet
    # variant('egl', default=False, description="Enable the EGL frontend.")

    # TODO: Effectively deal with hardware drivers
    # The implication of this is enabling DRI, among other things, and
    # needing to check which llvm targets were built (ptx or amdgpu, etc.)

    # Back ends
    variant('opengl', default=True, description="Enable full OpenGL support.")
    variant('opengles', default=False, description="Enable OpenGL ES support.")

    # Provides
    provides('gl@4.5',  when='+opengl')
    provides('glx@1.4', when='+glx')
    # provides('egl@1.5', when='+egl')
    provides('osmesa', when='+osmesa')

    # Variant dependencies
    depends_on('llvm@6:10', when='+llvm')
    depends_on('libx11',  when='+glx')
    depends_on('libxcb',  when='+glx')
    depends_on('libxext', when='+glx')
    depends_on('glproto@1.4.14:', when='+glx', type='build')

    # Prevent an unnecessary xcb-dri dependency
    patch('autotools-x11-nodri.patch')

    # Backport Mesa MR#6053 to prevent multiply-defined symbols
    patch('multiple-symbols_hash.patch', when='@:20.1.4%gcc@10:')

    def autoreconf(self, spec, prefix):
        which('autoreconf')('--force',  '--verbose', '--install')

    def configure_args(self):
        spec = self.spec
        args = [
            'LDFLAGS={0}'.format(self.spec['ncurses'].libs.search_flags),
            '--enable-shared',
            '--disable-static',
            '--disable-libglvnd',
            '--disable-nine',
            '--disable-omx-bellagio',
            '--disable-omx-tizonia',
            '--disable-opencl',
            '--disable-opencl-icd',
            '--disable-va',
            '--disable-vdpau',
            '--disable-xa',
            '--disable-xvmc',
            '--disable-osmesa',
            '--with-vulkan-drivers=']
        args_platforms = []
        args_gallium_drivers = ['swrast']
        args_dri_drivers = []

        if spec.target.family == 'arm' or spec.target.family == 'aarch64':
            args.append('--disable-libunwind')

        num_frontends = 0
        if '+osmesa' in spec:
            num_frontends += 1
            args.append('--enable-gallium-osmesa')
        else:
            args.append('--disable-gallium-osmesa')

        if '+glx' in spec:
            num_frontends += 1
            if '+egl' in spec:
                args.append('--enable-glx=dri')
            else:
                args.append('--enable-glx=gallium-xlib')
            args_platforms.append('x11')
        else:
            args.append('--disable-glx')

        if '+egl' in spec:
            num_frontends += 1
            args.extend(['--enable-egl', '--enable-gbm', '--enable-dri'])
            args_platforms.append('surfaceless')
        else:
            args.extend(['--disable-egl', '--disable-gbm', '--disable-dri'])

        if '+opengl' in spec:
            args.append('--enable-opengl')
        else:
            args.append('--disable-opengl')

        if '+opengles' in spec:
            args.extend(['--enable-gles1', '--enable-gles2'])
        else:
            args.extend(['--disable-gles1', '--disable-gles2'])

        if num_frontends > 1:
            args.append('--enable-shared-glapi')
        else:
            args.append('--disable-shared-glapi')

        if '+llvm' in spec:
            args.append('--enable-llvm')
            args.append('--with-llvm-prefix=%s' % spec['llvm'].prefix)
            if '+link_dylib' in spec['llvm']:
                args.append('--enable-llvm-shared-libs')
            else:
                args.append('--disable-llvm-shared-libs')
        else:
            args.append('--disable-llvm')

        args_swr_arches = []
        if 'swr=avx' in spec:
            args_swr_arches.append('avx')
        if 'swr=avx2' in spec:
            args_swr_arches.append('avx2')
        if 'swr=knl' in spec:
            args_swr_arches.append('knl')
        if 'swr=skx' in spec:
            args_swr_arches.append('skx')
        if args_swr_arches:
            if '+llvm' not in spec:
                raise SpecError('Variant swr requires +llvm')
            args_gallium_drivers.append('swr')
            args.append('--with-swr-archs=' + ','.join(args_swr_arches))

        # Add the remaining list args
        args.append('--with-platforms=' + ','.join(args_platforms))
        args.append('--with-gallium-drivers=' + ','.join(args_gallium_drivers))
        args.append('--with-dri-drivers=' + ','.join(args_dri_drivers))

        return args

    @property
    def libs(self):
        spec = self.spec
        libs_to_seek = set()

        if '+osmesa' in spec:
            libs_to_seek.add('libOSMesa')

        if '+glx' in spec:
            libs_to_seek.add('libGL')

        if '+opengl' in spec:
            libs_to_seek.add('libGL')

        if '+opengles' in spec:
            libs_to_seek.add('libGLES')
            libs_to_seek.add('libGLES2')

        if libs_to_seek:
            return find_libraries(list(libs_to_seek),
                                  root=self.spec.prefix,
                                  shared='+shared' in self.spec,
                                  recursive=True)
        return LibraryList()

    @property
    def osmesa_libs(self):
        return find_libraries('libOSMesa',
                              root=self.spec.prefix,
                              shared='+shared' in self.spec,
                              recursive=True)

    @property
    def glx_libs(self):
        return find_libraries('libGL',
                              root=self.spec.prefix,
                              shared='+shared' in self.spec,
                              recursive=True)

    @property
    def gl_libs(self):
        return find_libraries('libGL',
                              root=self.spec.prefix,
                              shared='+shared' in self.spec,
                              recursive=True)
