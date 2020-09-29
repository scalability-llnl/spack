# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import itertools
import sys


class Mesa(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL specification
     - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    maintainers = ['v-dobrev']

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
    variant('glvnd', default=is_linux,
            description="Expose Graphics APIs through libglvnd")
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
    provides('gl@4.5',  when='+opengl ~glvnd')
    provides('glx@1.4', when='+glx ~glvnd')
    # provides('egl@1.5', when='+egl ~glvnd')

    provides('libglvnd-be-gl', when='+opengl +glvnd')
    provides('libglvnd-be-glx', when='+opengl +glvnd +glx')
    # provides('libglvnd-be-egl', when='+opengl +glvnd +egl')

    # Variant dependencies
    depends_on('llvm@6:', when='+llvm')
    depends_on('libx11',  when='+glx')
    depends_on('libxcb',  when='+glx')
    depends_on('libxext', when='+glx')
    depends_on('glproto@1.4.14:', when='+glx', type='build')

    depends_on('libglvnd', when='+glvnd')

    # Add the necessary dri dependencies
    for dependency, constraint in itertools.product(
            ('damageproto@1.1:',
             'dri2proto@2.8:',
             'fixesproto',
             'glproto@1.4.13:',
             'libdrm@2.4.75:',
             'libx11',
             'libxext',
             'libxcb@1.8.1:',
             'libxdamage@1.1:',
             'libxfixes',
             'libxshmfence',
             'libxxf86vm',
             'xf86vidmodeproto'), ('+egl', '+glvnd')):
        depends_on(dependency, when=constraint)

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

        use_dri = ('+egl' in spec) or ('+glvnd' in spec)
        args.append('--enable-dri' if use_dri else '--disable-dri')

        if '+glvnd' in spec:
            args.append('--enable-libglvnd')
        else:
            args.append('--disable-libglvnd')

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

            args.append('--enable-glx=dri'
                        if use_dri else
                        '--enable-gxl=gallium-xlib')

            args_platforms.append('x11')
        else:
            args.append('--disable-glx')

        if '+egl' in spec:
            num_frontends += 1
            args.extend(['--enable-egl', '--enable-gbm'])
            args_platforms.append('surfaceless')
        else:
            args.extend(['--disable-egl', '--disable-gbm'])

        if '+opengl' in spec:
            args.append('--enable-opengl')
        else:
            args.append('--disable-opengl')

        if '+opengles' in spec:
            args.extend(['--enable-gles1', '--enable-gles2'])
        else:
            args.extend(['--disable-gles1', '--disable-gles2'])

        if num_frontends > 1 or ('+glvnd' in spec):
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

    # NOTE: Each of the following *libs properties return empty lists if
    # +glvnd, because there are no mesa libraries to be linked against.  When
    # acting as a glvnd dispatch target, libglvnd will find mesa's shared
    # objects via environment variables, dynamically load them, and dispatch
    # calls to them at run time.

    @property
    def libs(self):
        if '~glvnd' in self.spec:
            libs_to_seek = ['libGL']

            if '+osmesa' in self.spec:
                libs_to_seek.append('libOSMesa')

            if '+glx' in self.spec:
                libs_to_seek.append('libGLX')

            for dir in ['lib64', 'lib']:
                libs = find_libraries(libs_to_seek,
                                      join_path(self.spec.prefix, dir),
                                      shared='+shared' in self.spec,
                                      recursive=False)
                if libs:
                    return libs

        return LibraryList(())

    @property
    def gl_libs(self):
        if '+glvnd' in self.spec:
            return LibraryList(())

        return find_libraries('libGL',
                              root=self.spec.prefix,
                              shared='+shared' in self.spec,
                              recursive=True)

    @property
    def glx_libs(self):
        if '+glvnd' in self.spec:
            return LibraryList(())

        return find_libraries('libGLX',
                              root=self.spec.prefix,
                              shared='+shared' in self.spec,
                              recursive=True)

    def setup_run_environment(self, env):
        if '+glx +glvnd' in self.spec:
            env.set('__GLX_VENDOR_LIBRARY_NAME', 'mesa')

        if '+egl +glvnd' in self.spec:
            env.set('__EGL_VENDOR_LIBRARY_FILENAMES', ':'.join((
                os.path.join(self.spec.prefix, 'share', 'glvnd',
                             'egl_vendor.d', '50_mesa.json'))))
