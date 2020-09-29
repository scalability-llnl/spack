# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibglvndFe(BundlePackage):
    """The GL Vendor-Neutral Dispatch library (Frontend Dummy Package)

    libglvnd is a vendor-neutral dispatch layer for arbitrating OpenGL API
    calls between multiple vendors. It allows multiple drivers from different
    vendors to coexist on the same filesystem, and determines which vendor to
    dispatch each API call to at runtime.

    Both GLX and EGL are supported, in any combination with OpenGL and OpenGL
    ES."""

    homepage = "https://gitlab.freedesktop.org/glvnd/libglvnd"

    version('1.3.2')
    version('1.3.1')
    version('1.3.0')
    version('1.2.0')
    version('1.1.1')
    version('1.1.0')
    version('1.0.0')

    variant('glx', default=False, description='Provide GLX API')
    variant('egl', default=False, description='Provide EGL API')

    depends_on('libglvnd')

    depends_on('libglvnd-be-gl')
    depends_on('libglvnd-be-glx', when='+glx')
    depends_on('libglvnd-be-egl', when='+egl')

    # https://github.com/NVIDIA/libglvnd/blob
    #   /a4c332e3269ec5b1175f5fb63af99b070093adac
    #   /src/generate/genCommon.py#L39-L44
    provides('gl@1.0:1.5')
    provides('gl@2.0:2.1')
    provides('gl@3.0:3.3')
    provides('gl@4.0:4.5')

    provides('glx@1.4', when='+glx')
    provides('egl', when='+egl')

    @property
    def gl_libs(self):
        result = find_libraries('libOpenGL',
                              root=self.spec['libglvnd'].prefix,
                              shared=True,
                              recursive=True)
        print('\nexporting GL LIBS:\n')
        print('\n')
        print(result)
        print('\n')
        return result

    @property
    def glx_libs(self):
        result = find_libraries('libGLX',
                              root=self.spec['libglvnd'].prefix,
                              shared=True,
                              recursive=True)
        print('\nexporting GLX LIBS:\n')
        print('\n')
        print(result)
        print('\n')
        return result

    @property
    def egl_libs(self):
        result = find_libraries('libEGL',
                              root=self.spec['libglvnd'].prefix,
                              shared=True,
                              recursive=True)
        print('\nexporting EGL LIBS:\n')
        print('\n')
        print(result)
        print('\n')
        return result
