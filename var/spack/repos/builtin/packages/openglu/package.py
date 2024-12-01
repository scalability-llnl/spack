# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openglu(Package):
    """Placeholder for external OpenGL utility library (GLU) from hardware
    vendors"""

    homepage = "https://www.opengl.org/resources/libraries"

    provides("glu@:1.3", when="@1.3:")
    provides("glu@:1.2", when="@1.2:")
    provides("glu@:1.1", when="@1.1:")
    provides("glu@:1.0", when="@1.0:")

    # Override the fetcher method to throw a useful error message;
    # fixes an issue similar to Github issue (#7061), in which the
    # opengl package threw a generic, uninformative error message
    # during the `fetch` step
    @property
    def fetcher(self):
        msg = """This package is intended to be a placeholder for
        system-provided OpenGL utility (GLU) libraries from hardware vendors.
        Please download and install the GLU drivers/libraries for your
        graphics hardware separately, and then set that up as an external
        package.  An example of a working packages.yaml:

        packages:
          openglu:
            buildable: False
            externals:
            - spec: openglu@1.3
              prefix: /opt/opengl

        In that case, /opt/opengl/ should contain these two folders:

        include/GL/       (opengl headers, including "glu.h")
        lib               (opengl libraries, including "libGLU.so")

        On Apple Darwin (OS X, macOS) systems, this package is
        normally installed as part of the XCode Command Line Tools in
        /usr/X11R6, so a working packages.yaml would be

        packages:
          openglu:
            buildable: False
            externals:
            - spec: openglu@1.3
              prefix: /usr/X11R6

        In that case, /usr/X11R6 should contain

        include/GL       (GLU headers, including "glu.h")
        lib              (GLU libraries, including "libGLU.dylib")"""

        raise InstallError(msg)

    @fetcher.setter  # Since fetcher is read-write, must override both
    def fetcher(self):
        _ = self.fetcher

    @property
    def libs(self):
        return find_libraries("libGLU", self.prefix, shared=True, recursive=True)
