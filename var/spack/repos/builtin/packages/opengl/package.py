# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys


class Opengl(Package):
    """Placeholder for external OpenGL libraries from hardware vendors"""

    homepage = "https://www.opengl.org/"

    # Note that this is a dummy SHA since the package is strictly external
    version('4.5', sha256='0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')

    is_linux = sys.platform.startswith('linux')
    variant('glx', default=is_linux, description="Enable GLX API.")
    variant('egl', default=False, description="Enable EGL API.")
    variant('glvnd', default=is_linux,
            description="Expose Graphics APIs through libglvnd")

    provides('gl', when='~glvnd')
    provides('gl@:4.5', when='@4.5: ~glvnd')
    provides('gl@:4.4', when='@4.4: ~glvnd')
    provides('gl@:4.3', when='@4.3: ~glvnd')
    provides('gl@:4.2', when='@4.2: ~glvnd')
    provides('gl@:4.1', when='@4.1: ~glvnd')
    provides('gl@:3.3', when='@3.3: ~glvnd')
    provides('gl@:3.2', when='@3.2: ~glvnd')
    provides('gl@:3.1', when='@3.1: ~glvnd')
    provides('gl@:3.0', when='@3.0: ~glvnd')
    provides('gl@:2.1', when='@2.1: ~glvnd')
    provides('gl@:2.0', when='@2.0: ~glvnd')
    provides('gl@:1.5', when='@1.5: ~glvnd')
    provides('gl@:1.4', when='@1.4: ~glvnd')
    provides('gl@:1.3', when='@1.3: ~glvnd')
    provides('gl@:1.2', when='@1.2: ~glvnd')
    provides('gl@:1.1', when='@1.1: ~glvnd')
    provides('gl@:1.0', when='@1.0: ~glvnd')

    provides('glx@1.4', when='~glvnd +glx')
    provides('egl@1.5', when='~glvnd +egl')

    # NOTE: This package should have a dependency on libglvnd, but because it
    # is exclusively provided externally the dependency is never traversed.
    # depends_on('libglvnd', when='+glvnd')  # don't uncomment this

    provides('libglvnd-be-gl', when='+glvnd')
    provides('libglvnd-be-glx', when='+glvnd +glx')
    provides('libglvnd-be-egl', when='+glvnd +egl')

    executables = ['^glxinfo$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)(output=str, error=str)
        match = re.search(r'OpenGL version string: (\S+)', output)
        return match.group(1) if match else None

    # Override the fetcher method to throw a useful error message;
    # fixes GitHub issue (#7061) in which this package threw a
    # generic, uninformative error during the `fetch` step,
    @property
    def fetcher(self):
        msg = """This package is intended to be a placeholder for
        system-provided OpenGL libraries from hardware vendors.  Please
        download and install OpenGL drivers/libraries for your graphics
        hardware separately, and then set that up as an external package.
        An example of a working packages.yaml:

        packages:
          opengl:
            paths:
              opengl@4.5.0: /opt/opengl
            buildable: False

        In that case, /opt/opengl/ should contain these two folders:

        include/GL/       (opengl headers, including "gl.h")
        lib               (opengl libraries, including "libGL.so")

        On Apple Darwin (e.g., OS X, macOS) systems, this package is
        normally installed as part of the XCode Command Line Tools in
        /usr/X11R6, so a working packages.yaml would be

        packages:
          opengl:
            paths:
              opengl@4.1: /usr/X11R6
            buildable: False

        In that case, /usr/X11R6 should contain

        include/GL/      (OpenGL headers, including "gl.h")
        lib              (OpenGL libraries, including "libGL.dylib")

        On OS X/macOS, note that the version of OpenGL provided
        depends on your hardware. Look at
        https://support.apple.com/en-us/HT202823 to see what version
        of OpenGL your Mac uses."""
        raise InstallError(msg)

    @property
    def libs(self):
        result = LibraryList(())

        # "libs" provided by glvnd; this package sets the environment variables
        # so that glvnd, in turn, loads this package's libraries at run-time.
        if '+glvnd' in self.spec:
            return result

        for dir in ['lib64', 'lib']:
            libs = find_libraries('libGL', join_path(self.prefix, dir),
                                  shared=True, recursive=False)
            if libs:
                result.extend(libs)
                break

        if '+egl' in self.spec:
            for dir in ['lib64', 'lib']:
                libs = find_libraries('libEGL', join_path(self.prefix, dir),
                                      shared=True, recursive=False)
                if libs:
                    result.extend(libs)
                    break
        return result
