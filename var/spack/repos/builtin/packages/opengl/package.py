# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack.package import *


class Opengl(BundlePackage):
    """Placeholder for external OpenGL libraries from hardware vendors"""

    homepage = "https://www.opengl.org/"
    version("4.5")
    maintainers("biddisco")

    # This should really be when='platform=linux' but can't because of a
    # current bug in when and how ArchSpecs are constructed
    if sys.platform.startswith("linux"):
        provides("libglx")
        executables = ["^glxinfo$"]
    else:  # windows and mac
        provides("gl@4.5")

    @classmethod
    def determine_version(cls, exe):
        if exe:
            output = Executable(exe)(output=str, error=str)
            match = re.search(r"OpenGL version string: (\S+)", output)
            return match.group(1) if match else None
        else:
            return None

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

    @fetcher.setter  # Since fetcher is read-write, must override both
    def fetcher(self):
        _ = self.fetcher

    @property
    def headers(self):
        return self.gl_headers

    @property
    def libs(self):
        return self.gl_libs

    @property
    def gl_headers(self):
        spec = self.spec
        if "platform=darwin" in spec:
            header_name = "OpenGL/gl"
        else:
            header_name = "GL/gl"
        return find_headers(header_name, root=self.prefix, recursive=True)

    @property
    def gl_libs(self):
        spec = self.spec
        if "platform=windows" in spec:
            lib_name = "opengl32"
        elif "platform=darwin" in spec:
            lib_name = "libOpenGL"
        else:
            lib_name = "libGL"
        return find_libraries(lib_name, root=self.prefix, recursive=True)
