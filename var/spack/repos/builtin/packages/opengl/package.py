# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack.package import *


class Opengl(Package):
    """Placeholder for external OpenGL libraries from hardware vendors"""

    has_code = False

    homepage = "https://www.opengl.org/"

    provides('gl')
    provides('gl@:4.5', when='@4.5:')
    provides('gl@:4.4', when='@4.4:')
    provides('gl@:4.3', when='@4.3:')
    provides('gl@:4.2', when='@4.2:')
    provides('gl@:4.1', when='@4.1:')
    provides('gl@:3.3', when='@3.3:')
    provides('gl@:3.2', when='@3.2:')
    provides('gl@:3.1', when='@3.1:')
    provides('gl@:3.0', when='@3.0:')
    provides('gl@:2.1', when='@2.1:')
    provides('gl@:2.0', when='@2.0:')
    provides('gl@:1.5', when='@1.5:')
    provides('gl@:1.4', when='@1.4:')
    provides('gl@:1.3', when='@1.3:')
    provides('gl@:1.2', when='@1.2:')
    provides('gl@:1.1', when='@1.1:')
    provides('gl@:1.0', when='@1.0:')

    if sys.platform != 'darwin':
        provides('glx@1.4')

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
            buildable: False
            externals:
            - spec: opengl@4.5.0
              prefix: /opt/opengl

        In that case, /opt/opengl/ should contain these two folders:

        include/GL/       (opengl headers, including "gl.h")
        lib               (opengl libraries, including "libGL.so")

        On Apple Darwin (e.g., OS X, macOS) systems, this package is
        normally installed as part of the XCode Command Line Tools in
        /usr/X11R6, so a working packages.yaml would be

        packages:
          opengl:
            buildable: False
            externals:
            - spec: opengl@4.1
              prefix: /usr/X11R6

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
        return find_libraries(
            'libGL', self.prefix, shared=True, recursive=True)
