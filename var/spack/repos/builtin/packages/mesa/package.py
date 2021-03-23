# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys


class Mesa(MesonPackage):
    """Mesa is an open-source implementation of the OpenGL specification
     - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    maintainers = ['chuckatkins', 'v-dobrev']

    git = "https://gitlab.freedesktop.org/mesa/mesa.git"
    url = "https://archive.mesa3d.org/mesa-20.2.1.tar.xz"

    version('master', tag='master')
    version('20.2.1', sha256='d1a46d9a3f291bc0e0374600bdcb59844fa3eafaa50398e472a36fc65fd0244a')

    depends_on('meson@0.52:', type='build')

    depends_on('pkgconfig', type='build')
    depends_on('binutils', when=(sys.platform != 'darwin'), type='build')
    depends_on('bison', type='build')
    depends_on('cmake', type='build')
    depends_on('flex', type='build')
    depends_on('gettext', type='build')
    depends_on('python@3:', type='build')
    depends_on('py-mako@0.8.0:', type='build')
    depends_on('expat')
    depends_on('zlib@1.2.3:')

    # Internal options
    variant('llvm', default=True, description="Enable LLVM.")
    variant('swr', default='auto',
            values=('auto', 'none', 'avx', 'avx2', 'knl', 'skx'),
            multi=True,
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
    depends_on('llvm@6:', when='+llvm')
    depends_on('libx11',  when='+glx')
    depends_on('libxcb',  when='+glx')
    depends_on('libxext', when='+glx')
    depends_on('libxt',  when='+glx')
    depends_on('xrandr', when='+glx')
    depends_on('glproto@1.4.14:', when='+glx')

    # Require at least 1 front-end
    # TODO: Add egl to this conflict once made available
    conflicts('~osmesa ~glx')

    # Require at least 1 back-end
    # TODO: Add vulkan to this conflict once made available
    conflicts('~opengl ~opengles')

    # OpenGL ES requires OpenGL
    conflicts('~opengl +opengles')

    # 'auto' needed when shared llvm is built
    @when('^llvm~shared_libs')
    def patch(self):
        filter_file(
            r"_llvm_method = 'auto'",
            "_llvm_method = 'config-tool'",
            "meson.build")

    def meson_args(self):
        spec = self.spec
        args = [
            '-Dvulkan-drivers=',
            '-Dgallium-vdpau=disabled',
            '-Dgallium-xvmc=disabled',
            '-Dgallium-omx=disabled',
            '-Dgallium-va=disabled',
            '-Dgallium-xa=disabled',
            '-Dgallium-nine=false',
            '-Dgallium-opencl=disabled',
            '-Dbuild-tests=false',
            '-Dglvnd=false']
        args_platforms = []
        args_gallium_drivers = ['swrast']
        args_dri_drivers = []

        opt_enable = lambda c, o: '-D%s=%sabled' % (o, 'en' if c else 'dis')
        opt_bool = lambda c, o: '-D%s=%s' % (o, str(c).lower())
        if spec.target.family == 'arm' or spec.target.family == 'aarch64':
            args.append('-Dlibunwind=disabled')

        num_frontends = 0
        if '+osmesa' in spec:
            num_frontends += 1
            args.append('-Dosmesa=gallium')
        else:
            args.append('-Dosmesa=none')

        if '+glx' in spec:
            num_frontends += 1
            if '+egl' in spec:
                args.append('-Dglx=dri')
            else:
                args.append('-Dglx=gallium-xlib')
            args_platforms.append('x11')
        else:
            args.append('-Dglx=disabled')

        if '+egl' in spec:
            num_frontends += 1
            args.extend(['-Degl=enabled', '-Dgbm=enabled', '-Ddri3=enabled'])
            args_platforms.append('surfaceless')
        else:
            args.extend(
                ['-Degl=disabled', '-Dgbm=disabled', '-Ddri3=disabled'])

        args.append(opt_bool('+opengl' in spec, 'opengl'))
        args.append(opt_enable('+opengles' in spec, 'gles1'))
        args.append(opt_enable('+opengles' in spec, 'gles2'))

        args.append(opt_enable(num_frontends > 1, 'shared-glapi'))

        if '+llvm' in spec:
            args.append('-Dllvm=enabled')
            args.append(opt_enable(
                '+link_dylib' in spec['llvm'], 'shared-llvm'))
        else:
            args.append('-Dllvm=disabled')

        args_swr_arches = []
        if 'swr=auto' in spec:
            if 'avx' in spec.target:
                args_swr_arches.append('avx')
            if 'avx2' in spec.target:
                args_swr_arches.append('avx2')
            if 'avx512f' in spec.target:
                if 'avx512er' in spec.target:
                    args_swr_arches.append('knl')
                if 'avx512bw' in spec.target:
                    args_swr_arches.append('skx')
        else:
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
            args.append('-Dswr-arches=' + ','.join(args_swr_arches))

        # Add the remaining list args
        args.append('-Dplatforms=' + ','.join(args_platforms))
        args.append('-Dgallium-drivers=' + ','.join(args_gallium_drivers))
        args.append('-Ddri-drivers=' + ','.join(args_dri_drivers))

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
                                  recursive=True)
        return LibraryList()

    @property
    def osmesa_libs(self):
        return find_libraries('libOSMesa',
                              root=self.spec.prefix,
                              recursive=True)

    @property
    def glx_libs(self):
        return find_libraries('libGL',
                              root=self.spec.prefix,
                              recursive=True)

    @property
    def gl_libs(self):
        return find_libraries('libGL',
                              root=self.spec.prefix,
                              recursive=True)
